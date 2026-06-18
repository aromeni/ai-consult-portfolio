"""Synthetic capstone client data for Build 9 Phase 1."""


def get_synthetic_capstone_clients() -> list[dict]:
    return [
        {
            "client_id": "CAP001",
            "organisation_name": "BrightPath Skills Training",
            "sector": "Adult skills training",
            "staff_count": 8,
            "capstone_stage": "Implementation review",
            "primary_ai_goal": "Use AI safely for lesson planning, admin support, and staff productivity.",
            "consulting_priority": "Strengthen adoption evidence and standardise safe-use controls.",
        },
        {
            "client_id": "CAP002",
            "organisation_name": "Northside Community Advice",
            "sector": "Charity / advice service",
            "staff_count": 14,
            "capstone_stage": "Controlled rollout",
            "primary_ai_goal": "Improve document handling, internal guidance, and response drafting.",
            "consulting_priority": "Improve governance confidence before wider adoption.",
        },
        {
            "client_id": "CAP003",
            "organisation_name": "Greenacre Dental Group",
            "sector": "Healthcare administration",
            "staff_count": 22,
            "capstone_stage": "Governance-led pilot",
            "primary_ai_goal": "Use AI to reduce admin workload while keeping controls strong.",
            "consulting_priority": "Balance operational efficiency with responsible adoption controls.",
        },
    ]


def get_synthetic_cross_build_stages() -> list[dict]:
    return [
        # -------------------------------------------------------------------
        # BrightPath Skills Training (CAP001)
        # Showcase client — all stages completed with strong evidence.
        # Demonstrates the full end-to-end journey in a positive state.
        # -------------------------------------------------------------------
        {
            "stage_id": "STG001",
            "client_id": "CAP001",
            "organisation_name": "BrightPath Skills Training",
            "build_number": "Build 1",
            "build_name": "AI Readiness / Workflow Audit Tool",
            "journey_stage": "Readiness diagnosis",
            "stage_status": "Completed",
            "stage_summary": (
                "Initial workflow review identified lesson planning and admin tasks "
                "as suitable pilot areas."
            ),
            "evidence_strength": "Very strong",
            "consulting_value": "Created a clear, prioritised starting point for safe AI adoption.",
        },
        {
            "stage_id": "STG002",
            "client_id": "CAP001",
            "organisation_name": "BrightPath Skills Training",
            "build_number": "Build 2/3",
            "build_name": "Document Intelligence / Semantic RAG Policy Assistant",
            "journey_stage": "Document intelligence review",
            "stage_status": "Completed",
            "stage_summary": (
                "All training and policy documents were indexed and a retrieval layer "
                "demonstrated to staff. The reference system is integrated into the "
                "team's daily workflow."
            ),
            "evidence_strength": "Very strong",
            "consulting_value": (
                "Established a searchable knowledge base that staff use daily, reducing "
                "time spent locating guidance."
            ),
        },
        {
            "stage_id": "STG003",
            "client_id": "CAP001",
            "organisation_name": "BrightPath Skills Training",
            "build_number": "Build 4",
            "build_name": "AI Staff Training and Workshop Generator",
            "journey_stage": "Staff training",
            "stage_status": "Completed",
            "stage_summary": (
                "A 90-minute staff workshop on safe ChatGPT use for lesson planning and "
                "admin was delivered to all staff."
            ),
            "evidence_strength": "Very strong",
            "consulting_value": "Built staff confidence and established shared understanding of acceptable use.",
        },
        {
            "stage_id": "STG004",
            "client_id": "CAP001",
            "organisation_name": "BrightPath Skills Training",
            "build_number": "Build 5",
            "build_name": "AI Consulting Report Generator",
            "journey_stage": "Consulting report",
            "stage_status": "Completed",
            "stage_summary": (
                "A full consulting report was produced, reviewed by leadership, and "
                "signed off. It is used as the ongoing reference for the AI adoption plan."
            ),
            "evidence_strength": "Very strong",
            "consulting_value": "Delivered a polished, client-approved consulting report that anchors the entire adoption plan.",
        },
        {
            "stage_id": "STG005",
            "client_id": "CAP001",
            "organisation_name": "BrightPath Skills Training",
            "build_number": "Build 6",
            "build_name": "AI Governance Policy Checker",
            "journey_stage": "Governance review",
            "stage_status": "Completed",
            "stage_summary": (
                "Governance review completed. An acceptable-use policy and data boundary "
                "checklist were finalised and signed off by the principal."
            ),
            "evidence_strength": "Strong",
            "consulting_value": "Gave the organisation a documented governance position before confirming wider adoption.",
        },
        {
            "stage_id": "STG006",
            "client_id": "CAP001",
            "organisation_name": "BrightPath Skills Training",
            "build_number": "Build 7",
            "build_name": "AI Adoption ROI and Impact Tracker",
            "journey_stage": "Impact measurement",
            "stage_status": "Completed",
            "stage_summary": (
                "ROI measurement completed. Time savings of 3–5 hours per week per "
                "staff member have been confirmed across lesson planning and admin workflows."
            ),
            "evidence_strength": "Strong",
            "consulting_value": "Confirmed measurable returns on the AI adoption investment, supporting the internal business case.",
        },
        {
            "stage_id": "STG007",
            "client_id": "CAP001",
            "organisation_name": "BrightPath Skills Training",
            "build_number": "Build 8",
            "build_name": "AI Adoption Delivery and Implementation Tracker",
            "journey_stage": "Delivery tracking",
            "stage_status": "Completed",
            "stage_summary": (
                "All implementation actions are complete. Governance sign-off was received "
                "and staff adoption is confirmed across all agreed areas."
            ),
            "evidence_strength": "Strong",
            "consulting_value": "Demonstrated that recommendations were fully implemented with evidence and accountability.",
        },
        # -------------------------------------------------------------------
        # Northside Community Advice (CAP002)
        # Developing client — mostly completed but governance still under review.
        # Demonstrates a credible mid-journey with one area needing attention.
        # -------------------------------------------------------------------
        {
            "stage_id": "STG008",
            "client_id": "CAP002",
            "organisation_name": "Northside Community Advice",
            "build_number": "Build 1",
            "build_name": "AI Readiness / Workflow Audit Tool",
            "journey_stage": "Readiness diagnosis",
            "stage_status": "Completed",
            "stage_summary": (
                "Readiness review identified response drafting and internal guidance "
                "retrieval as priority AI use cases."
            ),
            "evidence_strength": "Strong",
            "consulting_value": (
                "Established a risk-aware adoption baseline for a client handling "
                "sensitive community data."
            ),
        },
        {
            "stage_id": "STG009",
            "client_id": "CAP002",
            "organisation_name": "Northside Community Advice",
            "build_number": "Build 2/3",
            "build_name": "Document Intelligence / Semantic RAG Policy Assistant",
            "journey_stage": "Document intelligence review",
            "stage_status": "Completed",
            "stage_summary": (
                "Internal guidance documents were indexed and a retrieval prototype "
                "was demonstrated to staff and management."
            ),
            "evidence_strength": "Strong",
            "consulting_value": (
                "Showed that AI-assisted document retrieval could improve consistency "
                "of advice without compromising client data."
            ),
        },
        {
            "stage_id": "STG010",
            "client_id": "CAP002",
            "organisation_name": "Northside Community Advice",
            "build_number": "Build 4",
            "build_name": "AI Staff Training and Workshop Generator",
            "journey_stage": "Staff training",
            "stage_status": "Completed",
            "stage_summary": (
                "A focused staff training session on safe AI use in advice contexts "
                "was delivered. Staff confirmed understanding of data boundaries and "
                "acceptable-use limits."
            ),
            "evidence_strength": "Moderate",
            "consulting_value": "Ensured staff understand both AI capabilities and data-privacy limits in sensitive advice environments.",
        },
        {
            "stage_id": "STG011",
            "client_id": "CAP002",
            "organisation_name": "Northside Community Advice",
            "build_number": "Build 5",
            "build_name": "AI Consulting Report Generator",
            "journey_stage": "Consulting report",
            "stage_status": "Completed",
            "stage_summary": (
                "A consulting report covering document intelligence findings and governance "
                "recommendations has been shared with the leadership team."
            ),
            "evidence_strength": "Moderate",
            "consulting_value": "Provided structured evidence to support a governance-first adoption approach.",
        },
        {
            "stage_id": "STG012",
            "client_id": "CAP002",
            "organisation_name": "Northside Community Advice",
            "build_number": "Build 6",
            "build_name": "AI Governance Policy Checker",
            "journey_stage": "Governance review",
            "stage_status": "Needs review",
            "stage_summary": (
                "Governance review highlighted gaps in data handling policy and approval "
                "processes. Further management input is needed before adoption proceeds."
            ),
            "evidence_strength": "Moderate",
            "consulting_value": "Prevented premature adoption by identifying governance blockers early.",
        },
        {
            "stage_id": "STG013",
            "client_id": "CAP002",
            "organisation_name": "Northside Community Advice",
            "build_number": "Build 7",
            "build_name": "AI Adoption ROI and Impact Tracker",
            "journey_stage": "Impact measurement",
            "stage_status": "Completed",
            "stage_summary": (
                "Initial ROI measurement completed. Time savings in response drafting "
                "and document retrieval have been estimated but not yet formally confirmed."
            ),
            "evidence_strength": "Moderate",
            "consulting_value": "Established a baseline for adoption evidence once the governance position is confirmed and wider rollout proceeds.",
        },
        {
            "stage_id": "STG014",
            "client_id": "CAP002",
            "organisation_name": "Northside Community Advice",
            "build_number": "Build 8",
            "build_name": "AI Adoption Delivery and Implementation Tracker",
            "journey_stage": "Delivery tracking",
            "stage_status": "Completed",
            "stage_summary": (
                "Delivery tracking is in place. The governance review action is the "
                "primary outstanding item. All other implementation actions have been "
                "assigned and tracked."
            ),
            "evidence_strength": "Moderate",
            "consulting_value": "Demonstrates organised implementation discipline even while governance is still being resolved.",
        },
        # -------------------------------------------------------------------
        # Greenacre Dental Group (CAP003)
        # Governance-strong client — excellent training and policy evidence
        # but delivery and ROI evidence are incomplete.
        # Demonstrates strong evidence in specific areas alongside gaps.
        # -------------------------------------------------------------------
        {
            "stage_id": "STG015",
            "client_id": "CAP003",
            "organisation_name": "Greenacre Dental Group",
            "build_number": "Build 1",
            "build_name": "AI Readiness / Workflow Audit Tool",
            "journey_stage": "Readiness diagnosis",
            "stage_status": "Completed",
            "stage_summary": (
                "Workflow audit identified appointment admin, patient communication "
                "templates, and internal reporting as safe AI use areas."
            ),
            "evidence_strength": "Strong",
            "consulting_value": (
                "Gave the practice a structured view of where AI could save time "
                "without touching clinical or patient data."
            ),
        },
        {
            "stage_id": "STG016",
            "client_id": "CAP003",
            "organisation_name": "Greenacre Dental Group",
            "build_number": "Build 2/3",
            "build_name": "Document Intelligence / Semantic RAG Policy Assistant",
            "journey_stage": "Document intelligence review",
            "stage_status": "In progress",
            "stage_summary": (
                "Internal admin templates and staff guidance documents are being reviewed "
                "for AI-assisted retrieval. Clinical records are strictly excluded."
            ),
            "evidence_strength": "Moderate",
            "consulting_value": "Demonstrates that document intelligence can be scoped responsibly in regulated environments.",
        },
        {
            "stage_id": "STG017",
            "client_id": "CAP003",
            "organisation_name": "Greenacre Dental Group",
            "build_number": "Build 4",
            "build_name": "AI Staff Training and Workshop Generator",
            "journey_stage": "Staff training",
            "stage_status": "Completed",
            "stage_summary": (
                "All admin staff completed a structured workshop on safe AI use. "
                "A written acceptable-use agreement was signed by each participant."
            ),
            "evidence_strength": "Very strong",
            "consulting_value": "Created auditable evidence of staff training, reducing liability risk for the practice.",
        },
        {
            "stage_id": "STG018",
            "client_id": "CAP003",
            "organisation_name": "Greenacre Dental Group",
            "build_number": "Build 5",
            "build_name": "AI Consulting Report Generator",
            "journey_stage": "Consulting report",
            "stage_status": "Completed",
            "stage_summary": (
                "A full consulting report covering readiness findings, safe-use boundaries, "
                "training outcomes, and governance recommendations was delivered."
            ),
            "evidence_strength": "Strong",
            "consulting_value": (
                "Provided a governance-ready document suitable for review by the practice "
                "owner and compliance contacts."
            ),
        },
        {
            "stage_id": "STG019",
            "client_id": "CAP003",
            "organisation_name": "Greenacre Dental Group",
            "build_number": "Build 6",
            "build_name": "AI Governance Policy Checker",
            "journey_stage": "Governance review",
            "stage_status": "Completed",
            "stage_summary": (
                "Governance review completed. An acceptable-use policy, data boundary "
                "checklist, and incident response guide have all been approved."
            ),
            "evidence_strength": "Very strong",
            "consulting_value": "Gave the practice a defensible governance position before committing to wider adoption.",
        },
        {
            "stage_id": "STG020",
            "client_id": "CAP003",
            "organisation_name": "Greenacre Dental Group",
            "build_number": "Build 7",
            "build_name": "AI Adoption ROI and Impact Tracker",
            "journey_stage": "Impact measurement",
            "stage_status": "Needs review",
            "stage_summary": (
                "ROI measurement is under review. Initial time savings in admin workflows "
                "are documented but require further verification before being formally "
                "confirmed in a regulated healthcare environment."
            ),
            "evidence_strength": "Moderate",
            "consulting_value": "Highlighted the importance of evidence verification before presenting ROI claims in a regulated environment.",
        },
        {
            "stage_id": "STG021",
            "client_id": "CAP003",
            "organisation_name": "Greenacre Dental Group",
            "build_number": "Build 8",
            "build_name": "AI Adoption Delivery and Implementation Tracker",
            "journey_stage": "Delivery tracking",
            "stage_status": "In progress",
            "stage_summary": (
                "Six implementation actions are actively tracked. Two governance sign-offs "
                "are outstanding. Staff training follow-up is scheduled for next month."
            ),
            "evidence_strength": "Moderate",
            "consulting_value": "Provided the practice with a structured delivery plan demonstrating consulting rigour and accountability.",
        },
    ]


def get_synthetic_capstone_indicators() -> list[dict]:
    return [
        {
            "client_id": "CAP001",
            "organisation_name": "BrightPath Skills Training",
            "readiness_position": "High readiness with confirmed AI adoption in place",
            "governance_position": "Governance approved and documented",
            "training_position": "All staff trained with confirmed adoption",
            "roi_position": "Confirmed ROI with measurable time savings",
            "delivery_position": "All implementation actions complete",
            "commercial_position": "Strong candidate for a capstone presentation and follow-up retainer",
            "overall_capstone_status": "Strong portfolio asset",
            "recommended_next_step": "Prepare the final capstone report and portfolio evidence pack for client presentation.",
        },
        {
            "client_id": "CAP002",
            "organisation_name": "Northside Community Advice",
            "readiness_position": "Moderate readiness with active adoption in controlled areas",
            "governance_position": "Governance gaps identified — review required before wider adoption",
            "training_position": "Staff trained with safe-use guidance in place",
            "roi_position": "Initial ROI estimates in place — formal confirmation pending",
            "delivery_position": "Delivery actions tracked — governance resolution outstanding",
            "commercial_position": "Governance improvement sprint recommended before wider engagement",
            "overall_capstone_status": "Developing demo",
            "recommended_next_step": "Resolve governance gaps and strengthen evidence before final client presentation.",
        },
        {
            "client_id": "CAP003",
            "organisation_name": "Greenacre Dental Group",
            "readiness_position": "High readiness with strong governance and training in place",
            "governance_position": "Governance approved and documented",
            "training_position": "All staff trained with written agreements",
            "roi_position": "ROI measurement under review — verification needed before confirming",
            "delivery_position": "Delivery actions in progress — documentation incomplete",
            "commercial_position": "Good candidate for a structured evidence review to confirm adoption returns",
            "overall_capstone_status": "Portfolio-ready demo",
            "recommended_next_step": "Complete document intelligence review and ROI measurement to strengthen the evidence base.",
        },
    ]
