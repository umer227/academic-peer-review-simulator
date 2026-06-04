from app.services.llm_service import llm_service


def generate_author_response(aggregated_review: str, decision: str) -> str:
    system = "You are an academic author drafting a professional response letter to reviewers."
    user = (
        "Write a polite, professional, detailed response letter with these sections: Greeting, Thanks to reviewers, "
        "Response to methodology comments, Response to originality/literature gap comments, "
        "Response to clarity/structure comments, Closing.\n\n"
        f"Decision:\n{decision}\n\nAggregated review:\n{aggregated_review}"
    )
    return llm_service.generate(system, user, "author")
