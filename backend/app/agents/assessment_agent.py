from app.services.llm_service import llm_service


def assess_paper(formatted_submission: str, aggregated_review: str, decision: str) -> str:
    system = (
        "You are an independent AI academic assessor providing a holistic quality evaluation "
        "of a manuscript after peer review has concluded. Your role is objective and constructive."
    )
    user = (
        "Provide an independent AI assessment of this manuscript. Use exactly these headings:\n"
        "Overall Quality Score, Publication Readiness, Key Strengths, Critical Gaps, Priority Recommendations\n\n"
        f"Manuscript:\n{formatted_submission}\n\n"
        f"Peer Review Summary:\n{aggregated_review}\n\n"
        f"Editorial Decision: {decision}"
    )
    return llm_service.generate(system, user, "assessment")
