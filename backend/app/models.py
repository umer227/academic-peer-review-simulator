from datetime import datetime

from sqlalchemy import DateTime, Integer, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class PaperReview(Base):
    __tablename__ = "paper_reviews"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    title: Mapped[str] = mapped_column(Text, nullable=False)
    abstract: Mapped[str] = mapped_column(Text, nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    domain: Mapped[str] = mapped_column(Text, nullable=False, default="Education")
    formatted_submission: Mapped[str] = mapped_column(Text, nullable=False)
    reviewer_1: Mapped[str] = mapped_column(Text, nullable=False)
    reviewer_2: Mapped[str] = mapped_column(Text, nullable=False)
    reviewer_3: Mapped[str] = mapped_column(Text, nullable=False)
    aggregated_review: Mapped[str] = mapped_column(Text, nullable=False)
    decision: Mapped[str] = mapped_column(Text, nullable=False)
    decision_reason: Mapped[str] = mapped_column(Text, nullable=False, default="")
    author_response_letter: Mapped[str] = mapped_column(Text, nullable=False)
    related_papers: Mapped[str] = mapped_column(Text, nullable=False, default="[]")
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)
