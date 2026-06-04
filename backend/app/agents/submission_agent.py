from app.schemas import PaperReviewRequest
from app.services.llm_service import llm_service


def format_submission(paper: PaperReviewRequest) -> str:
    system = "You are a submission editor preparing academic manuscripts for blinded peer review."
    user = (
        f"Format and validate this paper for review.\n\nTitle: {paper.title}\n"
        f"Domain: {paper.domain}\nAbstract: {paper.abstract}\n\nContent:\n{paper.content[:6000]}"
    )
    return llm_service.generate(system, user, "submission")
