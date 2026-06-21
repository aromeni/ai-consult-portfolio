"""
Report builder for Build 11.

Assembles a structured Markdown document intelligence report
from documents, retrieved evidence, Q&A output, and risk flags.
"""

from __future__ import annotations

from datetime import datetime


def build_report(
    documents: list[dict],
    query: str,
    answer_dict: dict,
    results: list[dict],
    risk_flags: list[dict],
    organisation_name: str = "BrightPath Skills Training",
) -> str:
    """
    Build and return a structured Markdown report string.

    Sections:
        1. Executive Summary
        2. Documents Analysed
        3. Question Asked
        4. Evidence Retrieved
        5. Grounded Answer
        6. Citations
        7. Governance and Risk Flags
        8. Recommended Next Steps
        9. Human Review Checklist
        10. Limitations and Responsible Use
    """
    timestamp = datetime.now().strftime("%d %B %Y, %H:%M")
    confidence = answer_dict.get("confidence", "insufficient")
    has_evidence = answer_dict.get("has_evidence", False)
    high_risks = sum(1 for f in risk_flags if f.get("risk_level") == "High")

    header = (
        f"# Document Intelligence Report\n\n"
        f"**Organisation:** {organisation_name}  \n"
        f"**Generated:** {timestamp}  \n"
        f"**Query:** {query}"
    )

    executive_summary = (
        f"## 1. Executive Summary\n\n"
        f"This report was generated in response to the query: *\"{query}\"*. "
        f"The document library contains {len(documents)} document(s). "
        f"{'Evidence was retrieved and an answer has been generated.' if has_evidence else 'No sufficient evidence was found to generate a grounded answer.'} "
        f"Answer confidence: **{confidence.capitalize()}**. "
        f"Governance review identified **{len(risk_flags)} risk flag(s)**"
        f"{f', including {high_risks} High-risk flag(s)' if high_risks else ''}."
    )

    sections = [
        header,
        executive_summary,
        f"## 2. Documents Analysed\n\n{_section_documents(documents)}",
        f"## 3. Question Asked\n\n> {query}",
        f"## 4. Evidence Retrieved\n\n{_section_evidence(results)}",
        f"## 5. Grounded Answer\n\n{answer_dict.get('answer', 'No answer generated.')}",
        f"## 6. Citations\n\n{_section_citations(answer_dict)}",
        f"## 7. Governance and Risk Flags\n\n{_section_risk_flags(risk_flags)}",
        f"## 8. Recommended Next Steps\n\n{_section_next_steps(answer_dict, risk_flags)}",
        f"## 9. Human Review Checklist\n\n{_section_human_review_checklist()}",
        f"## 10. Limitations and Responsible Use\n\n{_section_limitations()}",
    ]

    return "\n\n".join(sections)


def _section_documents(documents: list[dict]) -> str:
    """Format the documents-analysed section."""
    if not documents:
        return "_No documents loaded._"
    lines = []
    for i, doc in enumerate(documents, start=1):
        name = doc.get("source_name", doc.get("document_id", "Unknown"))
        words = doc.get("word_count", "—")
        lines.append(f"{i}. **{name}** ({words} words)")
    return "\n".join(lines)


def _section_evidence(results: list[dict]) -> str:
    """Format the retrieved evidence section."""
    if not results:
        return "_No evidence retrieved._"
    lines = []
    for r in results:
        source = r.get("source_name", "Unknown")
        chunk_id = r.get("chunk_id", "")
        score = r.get("score", 0.0)
        text = r.get("text", "")[:200]
        lines.append(
            f"**Rank {r.get('rank', '?')}** — {source} (score: {score:.3f})  \n"
            f"Chunk: `{chunk_id}`  \n"
            f"> {text}"
        )
    return "\n\n".join(lines)


def _section_citations(answer_dict: dict) -> str:
    """Format the citations section from an answer dict."""
    citations = answer_dict.get("citations", [])
    if not citations:
        return "_No citations available._"
    lines = []
    for i, cit in enumerate(citations, start=1):
        source = cit.get("source_name", "Unknown")
        chunk_id = cit.get("chunk_id", "")
        score = cit.get("score", 0.0)
        lines.append(f"{i}. **{source}** — chunk `{chunk_id}` (score: {score:.3f})")
    return "\n".join(lines)


def _section_risk_flags(risk_flags: list[dict]) -> str:
    """Format the governance and risk flags section."""
    if not risk_flags:
        return "_No governance risks identified in the retrieved evidence._"
    lines = []
    for flag in risk_flags:
        category = flag.get("category", "unknown").replace("_", " ").title()
        level = flag.get("risk_level", "Unknown")
        terms = ", ".join(flag.get("matched_terms", []))
        action = flag.get("recommended_action", "")
        lines.append(
            f"**{category}** — Risk level: {level}  \n"
            f"Matched terms: _{terms}_  \n"
            f"Recommended action: {action}"
        )
    return "\n\n".join(lines)


def _section_next_steps(answer_dict: dict, risk_flags: list[dict]) -> str:
    """Format the recommended next steps section."""
    steps = []
    high_risks = [f for f in risk_flags if f.get("risk_level") == "High"]

    if high_risks:
        steps.append(
            "- **Immediate:** Review all High-risk governance flags before distributing "
            "this output. Do not share AI-generated content relating to safeguarding, "
            "learner data, assessment decisions, or disciplinary matters without expert review."
        )

    if not answer_dict.get("has_evidence"):
        steps.append(
            "- **Search:** The query did not return sufficient evidence. "
            "Consider rephrasing the question or uploading additional relevant documents."
        )
    else:
        steps.append(
            "- **Verify:** A qualified staff member should review the grounded answer "
            "against the original source documents before acting on any guidance."
        )

    steps.append(
        "- **Document:** Record the use of this AI tool and the outcome of any human review "
        "in line with the organisation's AI acceptable use policy."
    )
    steps.append(
        "- **Escalate:** If any content in this report raises a safeguarding concern, "
        "follow the organisation's safeguarding procedures immediately."
    )

    return "\n".join(steps)


def _section_human_review_checklist() -> str:
    """Format the human review checklist section."""
    items = [
        "- [ ] The grounded answer has been read in full by a qualified reviewer.",
        "- [ ] All cited source documents have been consulted and verified.",
        "- [ ] Governance risk flags have been assessed and any required actions taken.",
        "- [ ] No identifiable personal or learner data appears in this output.",
        "- [ ] This report has been saved or distributed only through approved channels.",
        "- [ ] The AI acceptable use policy has been followed throughout this process.",
    ]
    return "\n".join(items)


def _section_limitations() -> str:
    """Return the standard limitations and responsible-use section."""
    return (
        "This report was generated using an AI-assisted document intelligence system. "
        "Answers are drawn exclusively from the documents uploaded to the library and "
        "are not verified by a subject-matter expert.\n\n"
        "**This report must not be used as the sole basis for decisions relating to "
        "learners, staff, safeguarding, assessment, or funding.** "
        "All AI-generated outputs must be reviewed and approved by a qualified "
        "member of staff before use or distribution.\n\n"
        "The system does not have access to real-time information, external databases, "
        "or any data outside the uploaded document library. "
        "It does not store or transmit personal data.\n\n"
        "*Generated by Build 11 — Production AI Document Intelligence and Governance Agent. "
        "For demonstration purposes only. "
        "All documents in the library are synthetic.*"
    )
