from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Paper
from app.schemas import PaperCreate, PaperListItem, PaperResponse, PaperResultResponse
from app.services.arxiv_service import search_related_papers


router = APIRouter(prefix="/papers", tags=["papers"])


def get_paper_or_404(paper_id: int, db: Session) -> Paper:
    paper = db.get(Paper, paper_id)
    if paper is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Paper not found")
    return paper


@router.post("/submit", response_model=PaperResponse, status_code=status.HTTP_201_CREATED)
def submit_paper(payload: PaperCreate, db: Session = Depends(get_db)):
    paper = Paper(
        title=payload.title,
        abstract=payload.abstract,
        keywords=payload.keywords,
        domain=payload.domain,
    )
    db.add(paper)
    db.commit()
    db.refresh(paper)
    return paper


@router.get("", response_model=list[PaperListItem])
def list_papers(db: Session = Depends(get_db)):
    return db.query(Paper).order_by(Paper.created_at.desc()).all()


@router.get("/search/arxiv")
def search_arxiv_papers(query: str = Query(..., min_length=1), max_results: int = Query(5, ge=3, le=5)):
    return search_related_papers(query=query, max_results=max_results)


@router.get("/{paper_id}", response_model=PaperResponse)
def get_paper(paper_id: int, db: Session = Depends(get_db)):
    return get_paper_or_404(paper_id, db)


@router.get("/{paper_id}/result", response_model=PaperResultResponse)
def get_paper_result(paper_id: int, db: Session = Depends(get_db)):
    paper = get_paper_or_404(paper_id, db)
    return {
        "paper": paper,
        "related_papers": paper.related_papers,
        "reviews": paper.reviews,
        "decision": paper.decision,
        "response_letter": paper.response_letter,
    }
