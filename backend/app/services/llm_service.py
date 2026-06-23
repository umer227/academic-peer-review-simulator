from __future__ import annotations

from openai import OpenAI
from anthropic import Anthropic

from app.config import get_settings


class LLMService:
    def __init__(self) -> None:
        self.settings = get_settings()
        self.openai_client = OpenAI(api_key=self.settings.openai_api_key) if self.settings.openai_api_key else None
        self.anthropic_client = Anthropic(api_key=self.settings.anthropic_api_key) if self.settings.anthropic_api_key else None

    @property
    def live_mode_enabled(self) -> bool:
        return bool(self.openai_client or self.anthropic_client)

    def generate(self, system_prompt: str, user_prompt: str, fallback_label: str) -> str:
        if self.openai_client:
            try:
                response = self.openai_client.chat.completions.create(
                    model="gpt-4o",
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": user_prompt},
                    ],
                    temperature=0.25,
                )
                return response.choices[0].message.content or self._mock_response(fallback_label)
            except Exception:
                pass

        if self.anthropic_client:
            try:
                response = self.anthropic_client.messages.create(
                    model="claude-3-5-sonnet-20241022",
                    max_tokens=1100,
                    temperature=0.25,
                    system=system_prompt,
                    messages=[{"role": "user", "content": user_prompt}],
                )
                return "\n".join(block.text for block in response.content if getattr(block, "type", "") == "text")
            except Exception:
                pass

        return self._mock_response(fallback_label)

    def _mock_response(self, label: str) -> str:
        responses = {
            "submission": (
                "Formatted Submission\n\n"
                "The manuscript has sufficient academic structure for simulated review. The title, abstract, "
                "research domain, and main body were normalized into a review-ready packet. The submission would "
                "benefit from explicit research questions, a concise method summary, and clearer contribution claims."
            ),
            "methodology": (
                "Strengths\n"
                "- The paper addresses a relevant educational problem with a coherent applied framing.\n"
                "- The proposed workflow is understandable and suitable for classroom experimentation.\n\n"
                "Weaknesses\n"
                "- The methodology does not yet define participants, data sources, metrics, or validity threats in enough detail.\n"
                "- The evaluation design needs clearer procedures for reproducibility.\n\n"
                "Suggestions\n"
                "- Add a dedicated methods section covering sampling, instruments, procedure, measures, and analysis plan.\n"
                "- Include limitations tied to classroom context, sample size, and assessment reliability.\n\n"
                "Score out of 10\n"
                "7/10\n\n"
                "Recommendation\n"
                "Minor Revision"
            ),
            "originality": (
                "Strengths\n"
                "- The topic is timely within AI-assisted education, formative feedback, and reflective learning research.\n"
                "- The manuscript has a plausible practical contribution for scalable peer feedback.\n\n"
                "Weaknesses\n"
                "- The literature gap is asserted more strongly than it is evidenced.\n"
                "- The current positioning should compare against recent peer feedback, learning analytics, and AI tutoring work.\n\n"
                "Suggestions\n"
                "- Add a related work subsection that contrasts the system with at least three recent research directions.\n"
                "- State the original contribution in one precise, testable paragraph.\n\n"
                "Score out of 10\n"
                "7/10\n\n"
                "Recommendation\n"
                "Minor Revision"
            ),
            "clarity": (
                "Strengths\n"
                "- The manuscript is readable and grounded in an accessible educational motivation.\n"
                "- The intended educational impact is relevant for instructors and learners.\n\n"
                "Weaknesses\n"
                "- Some claims need stronger transitions between problem, intervention, and evaluation.\n"
                "- The structure would benefit from clearer section headings and more explicit learner context.\n\n"
                "Suggestions\n"
                "- Add section headings for problem, intervention, implementation, evaluation, and limitations.\n"
                "- Define target learners and connect outcomes to practical teaching use.\n\n"
                "Score out of 10\n"
                "8/10\n\n"
                "Recommendation\n"
                "Minor Revision"
            ),
            "aggregator": (
                "Overall Summary\n"
                "The reviewers agree that the manuscript has a valuable educational motivation and a workable research direction.\n\n"
                "Common Strengths\n"
                "- Timely focus on AI-assisted educational feedback.\n"
                "- Clear potential value for instructors, learners, and classroom-scale formative assessment.\n\n"
                "Major Concerns\n"
                "- Methodological details are incomplete.\n"
                "- The literature gap needs stronger evidence from recent related work.\n"
                "- The manuscript structure should better connect problem, intervention, evaluation, and impact.\n\n"
                "Required Revisions\n"
                "- Clarify research questions, study design, participants, data sources, metrics, and limitations.\n"
                "- Expand related work and state the contribution precisely.\n"
                "- Improve section organization and transitions.\n\n"
                "Final Reviewer Consensus\n"
                "The paper should proceed after targeted revisions. The concerns are important but correctable."
            ),
            "decision": (
                "Decision: Minor Revision\n"
                "Reason: The paper shows promise and is suitable for continued consideration after targeted revisions. "
                "The concerns involve methodology detail, literature positioning, and clarity rather than a fundamental flaw."
            ),
            "assessment": (
                "Overall Quality Score\n"
                "7.3 / 10\n\n"
                "Publication Readiness\n"
                "Minor Revisions Needed — The manuscript demonstrates a sound educational motivation and a viable research direction. "
                "Targeted improvements to methodology, literature positioning, and structural clarity are required before publication.\n\n"
                "Key Strengths\n"
                "- Addresses a timely and practically relevant problem in AI-assisted formative feedback.\n"
                "- Workflow design is accessible and suitable for real classroom experimentation.\n"
                "- Clear alignment between the proposed intervention and measurable learner outcomes.\n\n"
                "Critical Gaps\n"
                "- Research questions are not formally stated; the study design lacks specificity on participants and metrics.\n"
                "- The literature review does not adequately situate the work against recent AI-in-education and peer feedback studies.\n"
                "- Validity threats, limitations, and reproducibility conditions are absent from the current draft.\n\n"
                "Priority Recommendations\n"
                "1. Add a dedicated Research Questions section with testable, measurable objectives.\n"
                "2. Expand the related work section to cover at least 5 recent studies (2021–2024) on AI feedback, peer assessment, and reflective learning.\n"
                "3. Include a full Methods section: participants, study design, instruments, data collection, analysis plan, and ethical considerations.\n"
                "4. State the contribution claim in one concise paragraph that differentiates this work from existing approaches.\n"
                "5. Restructure the manuscript with explicit section headings: Introduction, Related Work, Methodology, Expected Results, Limitations, Conclusion."
            ),
            "author": (
                "Dear Editors and Reviewers,\n\n"
                "Thank you for the careful and constructive review of our manuscript. We appreciate the reviewers' "
                "recognition of the educational relevance of the work and the practical value of improving peer feedback.\n\n"
                "Response to methodology comments\n"
                "We will expand the methodology section to specify participants, classroom context, data sources, "
                "rubric design, evaluation metrics, analysis procedures, and threats to validity. We will also include "
                "a clearer reproducibility description of the intervention workflow.\n\n"
                "Response to originality and literature gap comments\n"
                "We will strengthen the related work section by comparing our approach with recent research on AI-assisted "
                "feedback, learning analytics, peer assessment, and reflective learning. We will also revise the contribution "
                "statement to identify the specific research gap addressed by the manuscript.\n\n"
                "Response to clarity and structure comments\n"
                "We will reorganize the manuscript with clearer section headings, stronger transitions, and a more explicit "
                "connection between problem, intervention, evaluation, and educational impact.\n\n"
                "Closing\n"
                "We thank the reviewers again for their detailed guidance. We believe these revisions will substantially "
                "improve the clarity, rigor, and scholarly positioning of the paper.\n\nSincerely,\nThe Authors"
            ),
        }
        return responses.get(label, "Professional mock response generated for local demo mode.")


llm_service = LLMService()
