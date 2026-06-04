import json
import re

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.agents.aggregator_agent import aggregate_reviews
from app.agents.author_agent import generate_author_response
from app.agents.decision_agent import parse_decision, recommend_decision
from app.agents.reviewer_agents import review_clarity, review_methodology, review_originality
from app.agents.submission_agent import format_submission
from app.database import get_db
from app.models import PaperReview
from app.schemas import PaperReviewRequest, PaperReviewResponse, ReviewHistoryItem
from app.services.arxiv_service import search_arxiv
from app.services.crossref_service import search_crossref
from app.services.semantic_scholar_service import search_semantic_scholar

router = APIRouter(prefix="/api", tags=["reviews"])


def clean_related_title(title: str | None) -> str:
    value = " ".join((title or "Untitled paper").split())
    value = re.sub(r"^[\W_]+", "", value)
    value = re.sub(r"^\d+(?=[A-Z][a-z])", "", value)
    value = re.sub(r"^\d+[\.\)\]\-:\s]+", "", value)
    return value.strip() or "Untitled paper"


def clean_related_paper(paper: dict) -> dict:
    return {
        "title": clean_related_title(paper.get("title")),
        "authors": paper.get("authors") or [],
        "year": paper.get("year") or "N/A",
        "doi": paper.get("doi") or paper.get("DOI") or "N/A",
        "url": paper.get("url") or paper.get("URL") or None,
        "source": paper.get("source") or "N/A",
    }


def serialize_review(review: PaperReview) -> PaperReviewResponse:
    try:
        related = [clean_related_paper(item) for item in json.loads(review.related_papers or "[]")]
    except json.JSONDecodeError:
        related = []
    return PaperReviewResponse(
        id=review.id,
        paper_id=review.id,
        title=review.title,
        abstract=review.abstract,
        content=review.content,
        domain=review.domain,
        formatted_submission=review.formatted_submission,
        reviewer_1=review.reviewer_1,
        reviewer_2=review.reviewer_2,
        reviewer_3=review.reviewer_3,
        aggregated_review=review.aggregated_review,
        decision=review.decision,
        decision_reason=review.decision_reason,
        author_response_letter=review.author_response_letter,
        related_papers=related,
        created_at=review.created_at,
    )


@router.post("/review-paper", response_model=PaperReviewResponse)
async def review_paper(payload: PaperReviewRequest, db: Session = Depends(get_db)):
    arxiv, semantic, crossref = await search_arxiv(payload.title, payload.domain), await search_semantic_scholar(payload.title, payload.domain), await search_crossref(payload.title, payload.domain)
    related_papers = [clean_related_paper(paper) for paper in (arxiv + semantic + crossref)[:8]]

    formatted = format_submission(payload)
    reviewer_1 = review_methodology(formatted)
    reviewer_2 = review_originality(formatted, related_papers)
    reviewer_3 = review_clarity(formatted)
    aggregated = aggregate_reviews(reviewer_1, reviewer_2, reviewer_3)
    decision_text = recommend_decision(aggregated)
    decision, decision_reason = parse_decision(decision_text)
    author_response = generate_author_response(aggregated, f"{decision}\n\nReason: {decision_reason}")

    review = PaperReview(
        title=payload.title,
        abstract=payload.abstract,
        content=payload.content,
        domain=payload.domain,
        formatted_submission=formatted,
        reviewer_1=reviewer_1,
        reviewer_2=reviewer_2,
        reviewer_3=reviewer_3,
        aggregated_review=aggregated,
        decision=decision,
        decision_reason=decision_reason,
        author_response_letter=author_response,
        related_papers=json.dumps(related_papers),
    )
    db.add(review)
    db.commit()
    db.refresh(review)
    return serialize_review(review)


@router.get("/reviews", response_model=list[ReviewHistoryItem])
def list_reviews(db: Session = Depends(get_db)):
    reviews = db.query(PaperReview).order_by(PaperReview.created_at.desc()).all()
    return [
        ReviewHistoryItem(
            paper_id=review.id,
            title=review.title,
            domain=review.domain,
            decision=review.decision,
            created_at=review.created_at,
        )
        for review in reviews
    ]


@router.get("/reviews/{paper_id}", response_model=PaperReviewResponse)
def get_review(paper_id: int, db: Session = Depends(get_db)):
    review = db.get(PaperReview, paper_id)
    if not review:
        raise HTTPException(status_code=404, detail="Review not found")
    return serialize_review(review)
