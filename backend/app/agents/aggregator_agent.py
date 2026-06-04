from app.services.llm_service import llm_service


def aggregate_reviews(reviewer_1: str, reviewer_2: str, reviewer_3: str) -> str:
    system = "You are an academic area chair consolidating multiple reviewer reports."
    user = (
        "Combine the three reviews into a concise meta-review. Remove duplicates, highlight consensus, "
        "and list the highest-priority revisions. Use exactly these headings: Overall Summary, Common Strengths, "
        "Major Concerns, Required Revisions, Final Reviewer Consensus.\n\n"
        f"Reviewer 1:\n{reviewer_1}\n\nReviewer 2:\n{reviewer_2}\n\nReviewer 3:\n{reviewer_3}"
    )
    return llm_service.generate(system, user, "aggregator")
