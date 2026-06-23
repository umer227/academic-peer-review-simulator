from datetime import datetime
from typing import Any

from pydantic import BaseModel, Field


class PaperReviewRequest(BaseModel):
    title: str = Field(..., min_length=3)
    abstract: str = Field(..., min_length=10)
    content: str = Field(..., min_length=30)
    domain: str = "Education"


class RelatedPaper(BaseModel):
    title: str
    authors: list[str] = []
    year: str | int | None = None
    url: str | None = None
    source: str


class PaperReviewResponse(BaseModel):
    id: int
    paper_id: int
    title: str
    abstract: str
    content: str
    domain: str
    formatted_submission: str
    reviewer_1: str
    reviewer_2: str
    reviewer_3: str
    aggregated_review: str
    decision: str
    decision_reason: str = ""
    author_response_letter: str
    related_papers: list[dict[str, Any]] = []
    ai_assessment: str = ""
    created_at: datetime | None = None


class ReviewHistoryItem(BaseModel):
    paper_id: int
    title: str
    domain: str
    decision: str
    created_at: datetime
