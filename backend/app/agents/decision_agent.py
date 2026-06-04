import re

from app.services.llm_service import llm_service


VALID_DECISIONS = ("Accept", "Minor Revision", "Major Revision", "Reject")


def recommend_decision(aggregated_review: str) -> str:
    system = "You are a program committee decision agent. Choose Accept, Minor Revision, Major Revision, or Reject."
    user = (
        "Make a final recommendation and explain the rationale. Format as:\n"
        "Decision: <Accept|Minor Revision|Major Revision|Reject>\n"
        "Reason: <one or two concise sentences>\n\n"
        f"{aggregated_review}"
    )
    response = llm_service.generate(system, user, "decision")
    for decision in VALID_DECISIONS:
        if decision.lower() in response.lower():
            return response if response.strip() != decision else f"Decision: {decision}\nReason: The review supports this outcome."
    return "Decision: Minor Revision\nReason: The review identifies fixable issues and recommends targeted revision."


def parse_decision(decision_text: str) -> tuple[str, str]:
    decision = "Minor Revision"
    for option in VALID_DECISIONS:
        if re.search(rf"\b{re.escape(option)}\b", decision_text, flags=re.IGNORECASE):
            decision = option
            break

    reason_match = re.search(r"Reason:\s*(.+)", decision_text, flags=re.IGNORECASE | re.DOTALL)
    if reason_match:
        reason = reason_match.group(1).strip()
    else:
        lines = [line.strip() for line in decision_text.splitlines() if line.strip()]
        reason = " ".join(line for line in lines if decision.lower() not in line.lower()).strip()
    return decision, reason or "The reviewers identified correctable issues that can be addressed in revision."
