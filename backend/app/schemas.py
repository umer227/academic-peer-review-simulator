from datetime import datetime

from pydantic import BaseModel


class HealthResponse(BaseModel):
    status: str
    service: str
    environment: str


class PaperCreate(BaseModel):
    title: str
    abstract: str
    keywords: str | None = None
    domain: str


class PaperResponse(BaseModel):
    id: int
    title: str
    abstract: str
    keywords: str | None
    domain: str
    created_at: datetime

    model_config = {"from_attributes": True}


class PaperListItem(BaseModel):
    id: int
    title: str
    domain: str
    created_at: datetime

    model_config = {"from_attributes": True}


class ReviewResponse(BaseModel):
    id: int
    paper_id: int
    reviewer_name: str | None
    reviewer_role: str | None
    score: float | None
    recommendation: str | None
    strengths: str | None
    weaknesses: str | None
    questions: str | None
    full_review: str | None
    created_at: datetime

    model_config = {"from_attributes": True}


class DecisionResponse(BaseModel):
    id: int
    paper_id: int
    final_decision: str | None
    confidence_score: float | None
    reason: str | None
    aggregated_summary: str | None
    created_at: datetime

    model_config = {"from_attributes": True}


class ResponseLetterResponse(BaseModel):
    id: int
    paper_id: int
    letter_text: str | None
    created_at: datetime

    model_config = {"from_attributes": True}


class RelatedPaperResponse(BaseModel):
    id: int
    paper_id: int
    source: str | None
    title: str | None
    authors: str | None
    year: str | None
    url: str | None
    summary: str | None
    created_at: datetime

    model_config = {"from_attributes": True}


class PaperResultResponse(BaseModel):
    paper: PaperResponse
    related_papers: list[RelatedPaperResponse]
    reviews: list[ReviewResponse]
    decision: DecisionResponse | None
    response_letter: ResponseLetterResponse | None
