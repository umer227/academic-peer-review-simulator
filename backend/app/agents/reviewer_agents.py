from app.services.llm_service import llm_service


def review_methodology(formatted_submission: str) -> str:
    system = "You are Reviewer 1, an expert academic methodology reviewer."
    user = (
        "Evaluate methodology, technical correctness, validity, metrics, and limitations. "
        "Use exactly these headings: Strengths, Weaknesses, Suggestions, Score out of 10, Recommendation.\n\n"
        f"{formatted_submission}"
    )
    return llm_service.generate(system, user, "methodology")


def review_originality(formatted_submission: str, related_papers: list[dict]) -> str:
    system = "You are Reviewer 2, an expert in originality, literature gaps, and research positioning."
    user = (
        "Evaluate novelty, literature gap, contribution, and missing citations. "
        "Use exactly these headings: Strengths, Weaknesses, Suggestions, Score out of 10, Recommendation. "
        "Consider these related papers:\n"
        f"{related_papers}\n\nSubmission:\n{formatted_submission}"
    )
    return llm_service.generate(system, user, "originality")


def review_clarity(formatted_submission: str) -> str:
    system = "You are Reviewer 3, an expert in academic clarity, structure, and educational impact."
    user = (
        "Evaluate writing quality, organization, readability, and educational value. "
        "Use exactly these headings: Strengths, Weaknesses, Suggestions, Score out of 10, Recommendation.\n\n"
        f"{formatted_submission}"
    )
    return llm_service.generate(system, user, "clarity")
