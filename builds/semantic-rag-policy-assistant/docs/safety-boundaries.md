# Safety Boundaries — Semantic RAG Policy Assistant

**Build 3 · BrightPath ChatGPT Mastery Project**

---

## Core Safety Rule

> **Use synthetic or approved documents only. Do not upload, paste, or process real learner data, safeguarding case details, confidential client records, staff HR data, personal data, or regulated information.**

This boundary applies at every phase of this build, regardless of which features are active.

---

## What This Prototype Uses

- Synthetic Markdown policy documents (fictional, clearly labelled)
- Local deterministic keyword search (Phase 1 — complete)
- Local word-based chunking with configurable overlap and section strategy (Phase 2 — complete)
- Local embeddings via sentence-transformers/all-MiniLM-L6-v2, 384-dimensional vectors (Phase 3 — complete, no external API)
- Local FAISS vector index — IndexFlatIP (cosine) and IndexFlatL2 (Phase 4 — complete, no cloud service)
- Semantic search via query embedding and FAISS nearest-neighbour retrieval (Phase 5 — complete)
- Deterministic template-based RAG Q&A with intent detection and evidence grounding (Phase 6 — complete, no LLM API)
- Keyword vs semantic retrieval comparison with overlap detection (Phase 7 — complete)
- 10-section downloadable Markdown answer report (Phase 8 — complete)

---

## What This Prototype Does NOT Use

- External AI APIs (OpenAI, Anthropic, Cohere, Google, Azure AI, etc.) — not in any phase
- Cloud-hosted embedding services
- Real learner data of any kind
- Safeguarding information or welfare case records
- Confidential client records or commercially sensitive information
- Staff HR, performance, or disciplinary records
- Personal data (any information that could identify a living individual)
- Regulated information (health, financial, legal, or data-protection-regulated content)
- Authentication or access control (prototype only — not for multi-user deployment)
- Database functionality
- Production cloud deployment

---

## Prohibited Uses

The following uses are strictly prohibited at every phase of this build:

1. Uploading, pasting, or processing real learner names, records, contact details, grades, or attendance
2. Uploading, pasting, or processing safeguarding disclosures, concerns, welfare referrals, or case notes
3. Uploading, pasting, or processing confidential client contracts, pricing, or commercial strategy
4. Uploading, pasting, or processing staff HR files, appraisals, disciplinary records, or performance data
5. Uploading, pasting, or processing personal data that could identify any living individual
6. Uploading, pasting, or processing regulated information of any kind
7. Using this tool to make or support live safeguarding, HR, compliance, clinical, or legal decisions
8. Claiming this tool's outputs are professionally authoritative without qualified human review
9. Deploying this prototype as a production system without a full DPIA and legal review

---

## Human Review Required

All outputs from this tool — search results, retrieved chunks, generated answers, and reports — are starting points for human review, not final authority. A qualified human professional must review, verify, and take responsibility for any decision informed by this tool's outputs.

---

## Output Limitations

This prototype does not provide:

- Legal advice or compliance assessments
- Safeguarding guidance or decisions
- HR or employment decisions
- Clinical, medical, or health guidance
- Financial advice
- Academic integrity decisions
- Any other form of professional advice

---

## Data Protection Guidance for Future Phases

If this architecture is ever adapted for real organisational documents, the following steps are required before processing any personal or sensitive data:

1. Conduct a Data Protection Impact Assessment (DPIA)
2. Obtain qualified data protection and legal review
3. Add authentication, access control, and audit logging
4. Implement secure document upload and storage
5. Define and enforce data retention and deletion policies
6. Establish incident reporting and breach notification procedures
7. Confirm compliance with applicable data protection law (e.g. UK GDPR)

No production deployment should proceed without all of the above in place.

---

*Build 3 · Semantic RAG Policy Assistant · BrightPath ChatGPT Mastery Project*
*All documents used in this prototype are synthetic and for demonstration purposes only.*
