"""Synthetic demo audit data for Build 5 — AI Consulting Report Generator.

All data is fictional. No real organisation, client, learner, HR, or personal data.
BrightPath Skills Training is a synthetic scenario used throughout the ChatGPT Mastery portfolio.
"""


def get_brightpath_audit_data() -> dict:
    """Return the full synthetic BrightPath AI readiness audit dataset."""
    return {
        "organisation_profile": {
            "organisation_name": "BrightPath Skills Training",
            "organisation_type": "Private training provider",
            "sector": "Education and Training",
            "country_context": "United Kingdom",
            "staff_count": 24,
            "departments": [
                "Curriculum and Learning Design",
                "Learner Support",
                "Administration and Operations",
                "Business Development",
                "Quality and Compliance",
            ],
            "current_ai_use": (
                "Informal use of ChatGPT by some staff for lesson planning, "
                "email drafting, and report writing. No organisational policy in place. "
                "No formal governance or approved tools list."
            ),
            "main_business_goals": [
                "Improve quality and consistency of course materials",
                "Reduce administrative burden on tutors",
                "Scale learner support without increasing headcount",
                "Strengthen Ofsted readiness and quality assurance",
                "Remain competitive in a technology-led training market",
            ],
        },
        "readiness_scores": {
            "strategy_score": 32,
            "data_governance_score": 28,
            "staff_capability_score": 45,
            "workflow_opportunity_score": 68,
            "risk_management_score": 25,
            "leadership_alignment_score": 52,
            "overall_readiness_score": 42,
        },
        "workflow_findings": get_demo_workflow_findings(),
        "risk_findings": get_demo_risk_findings(),
        "pilot_recommendations": get_demo_pilot_recommendations(),
        "training_needs": get_demo_training_needs(),
        "governance_gaps": get_demo_governance_gaps(),
    }


def get_default_readiness_categories() -> list:
    """Return the standard readiness dimension labels."""
    return [
        "Strategy",
        "Data Governance",
        "Staff Capability",
        "Workflow Opportunity",
        "Risk Management",
        "Leadership Alignment",
    ]


def get_default_report_sections() -> list:
    """Return the standard client report section titles."""
    return [
        "Executive Summary",
        "Organisation Context",
        "AI Readiness Assessment",
        "Workflow Findings",
        "Key Risks",
        "Governance Gaps",
        "Recommended AI Opportunities",
        "Recommended Pilots",
        "Training Needs",
        "30/60/90-Day Roadmap",
        "Risk Register",
        "Next Steps",
        "Responsible-Use Boundaries",
        "Prototype Limitations",
    ]


def get_demo_workflow_findings() -> list:
    """Return synthetic workflow findings for BrightPath."""
    return [
        {
            "workflow_name": "Course Material Development",
            "current_process": (
                "Tutors manually draft lesson plans, slide decks, and handouts from scratch. "
                "No shared templates. Review process is ad hoc."
            ),
            "pain_points": [
                "High time cost per course — typically 8–12 hours per new unit",
                "Inconsistency between tutors in quality and format",
                "No systematic quality review before learner delivery",
            ],
            "ai_opportunity": (
                "AI-assisted first-draft generation for lesson plans and handouts using approved "
                "synthetic templates, followed by tutor review and customisation."
            ),
            "risk_level": "Medium",
            "potential_value": "High — could save 3–5 hours per unit per tutor",
            "recommended_action": (
                "Run a pilot using AI-generated lesson plan drafts with structured tutor "
                "review and sign-off before delivery."
            ),
        },
        {
            "workflow_name": "Learner Progress Report Writing",
            "current_process": (
                "Tutors write individual learner progress reports manually. Reports are submitted "
                "to the Quality Lead for review. Average time: 20 minutes per report."
            ),
            "pain_points": [
                "High administrative burden during reporting periods",
                "Risk of personal learner data being entered into unapproved tools",
                "Reports vary significantly in structure and depth",
            ],
            "ai_opportunity": (
                "AI-assisted report structure templates with approved generic language banks. "
                "Tutors populate learner-specific detail manually — no learner data in AI tools."
            ),
            "risk_level": "High",
            "potential_value": "Medium — reduces report writing time while managing data risk",
            "recommended_action": (
                "Develop approved report template with AI-generated generic language sections. "
                "Explicitly prohibit learner names or IDs in any AI tool."
            ),
        },
        {
            "workflow_name": "Enquiry and Enrolment Administration",
            "current_process": (
                "Enquiries arrive by phone, email, and website form. Administrators respond "
                "individually. Enrolment requires manual data entry into the MIS."
            ),
            "pain_points": [
                "Slow response times to enquiries outside office hours",
                "Repetitive email responses drain administrator time",
                "No self-service information for prospective learners",
            ],
            "ai_opportunity": (
                "AI-drafted FAQ and enquiry response templates; potential for a supervised "
                "chatbot for common course enquiries."
            ),
            "risk_level": "Low",
            "potential_value": "Medium — improves responsiveness and reduces admin load",
            "recommended_action": (
                "Draft AI-generated email response templates for common enquiry types. "
                "Review before deploying any automated response system."
            ),
        },
        {
            "workflow_name": "Quality and Compliance Reporting",
            "current_process": (
                "Quality Lead compiles inspection evidence manually from tutor records, "
                "observation notes, and learner feedback. Significant time investment pre-inspection."
            ),
            "pain_points": [
                "Compilation is slow and error-prone",
                "Evidence is stored inconsistently across staff",
                "AI tool use is untracked — creates compliance risk",
            ],
            "ai_opportunity": (
                "AI-assisted summarisation of compiled evidence documents (approved internal "
                "data only). AI use log for compliance evidence."
            ),
            "risk_level": "Medium",
            "potential_value": "High — reduces inspection preparation time significantly",
            "recommended_action": (
                "Introduce an AI use policy and log before any AI-assisted compliance work begins."
            ),
        },
    ]


def get_demo_risk_findings() -> list:
    """Return synthetic risk findings for BrightPath."""
    return [
        {
            "risk_title": "Learner Data in Unapproved AI Tools",
            "risk_category": "Data Protection",
            "likelihood": "High",
            "impact": "High",
            "risk_level": "Critical",
            "description": (
                "Staff are informally using ChatGPT without a policy. Learner names, attendance "
                "records, or progress data may have already been entered into external AI tools, "
                "constituting a potential GDPR breach."
            ),
            "recommended_control": (
                "Immediate policy intervention. Explicit prohibition on entering learner data "
                "into any external AI tool. Staff briefing before next term."
            ),
            "owner": "Quality and Compliance Lead",
        },
        {
            "risk_title": "No Approved AI Tools List",
            "risk_category": "Governance",
            "likelihood": "High",
            "impact": "Medium",
            "risk_level": "High",
            "description": (
                "No approved or unapproved tools list exists. Staff are using personal ChatGPT "
                "accounts, which fall outside organisational data agreements."
            ),
            "recommended_control": (
                "Establish an approved tools list in the AI policy. Include ChatGPT only under "
                "an approved business tier account with appropriate data processing agreements."
            ),
            "owner": "Senior Leadership Team",
        },
        {
            "risk_title": "AI Hallucination in Training Materials",
            "risk_category": "Quality and Accuracy",
            "likelihood": "Medium",
            "impact": "High",
            "risk_level": "High",
            "description": (
                "AI-generated content may contain factual errors or invented references, "
                "particularly in vocational and regulated areas. Learners could receive incorrect guidance."
            ),
            "recommended_control": (
                "Mandatory human review of all AI-generated content before learner delivery. "
                "Review checklist to be included in AI policy."
            ),
            "owner": "Curriculum Lead",
        },
        {
            "risk_title": "Safeguarding Decisions Delegated to AI",
            "risk_category": "Safeguarding",
            "likelihood": "Low",
            "impact": "Critical",
            "risk_level": "High",
            "description": (
                "No current evidence of this occurring, but absence of a policy creates the risk. "
                "Staff may seek AI guidance on learner safeguarding concerns rather than following "
                "proper escalation routes."
            ),
            "recommended_control": (
                "Explicit prohibition in AI policy: AI must not be used for any safeguarding "
                "concern, disclosure, or decision. Safeguarding contact details to be communicated "
                "alongside AI guidance."
            ),
            "owner": "Designated Safeguarding Lead",
        },
        {
            "risk_title": "Inconsistent AI Use Across Departments",
            "risk_category": "Operational",
            "likelihood": "High",
            "impact": "Low",
            "risk_level": "Medium",
            "description": (
                "Some departments are using AI tools regularly; others are not aware of them. "
                "This creates inconsistency in output quality and potential competitive disadvantage "
                "for non-using teams."
            ),
            "recommended_control": (
                "Organisation-wide AI awareness training and a shared responsible-use guide."
            ),
            "owner": "All Department Heads",
        },
    ]


def get_demo_pilot_recommendations() -> list:
    """Return synthetic pilot recommendations for BrightPath."""
    return [
        {
            "pilot_name": "AI-Assisted Lesson Plan Drafts",
            "business_problem": (
                "Tutors spend 8–12 hours creating new course units from scratch, "
                "with no shared templates or quality baseline."
            ),
            "proposed_solution": (
                "Provide tutors with an approved AI-assisted lesson plan generator "
                "(Build 4 prototype or equivalent) using synthetic scenarios. "
                "Tutors review, adapt, and sign off all outputs before delivery."
            ),
            "expected_benefits": [
                "Reduce lesson plan drafting time by 40–60%",
                "Improve consistency of course materials across tutors",
                "Create a foundation for a reusable curriculum template library",
            ],
            "complexity": "Low",
            "risk_level": "Low",
            "suggested_timeline": "Month 1–2",
            "success_measures": [
                "Average lesson plan drafting time reduced from 8 hours to under 4 hours",
                "All tutor sign-offs completed before delivery",
                "No learner data entered into AI tools",
            ],
        },
        {
            "pilot_name": "Email Response Templates",
            "business_problem": (
                "Administrators spend significant time writing repetitive responses to common "
                "enquiries about courses, enrolment, and funding."
            ),
            "proposed_solution": (
                "AI-generate a library of approved email response templates for the 15 most common "
                "enquiry types. Administrators use these as starting points, personalising as needed."
            ),
            "expected_benefits": [
                "Reduce enquiry response time by 30–50%",
                "Improve consistency and professionalism of written communications",
                "Free administrator time for higher-value tasks",
            ],
            "complexity": "Low",
            "risk_level": "Low",
            "suggested_timeline": "Month 1",
            "success_measures": [
                "Template library of 15 enquiry types created and approved",
                "Administrator adoption rate above 70% within 4 weeks",
                "Enquiry response time reduced by measurable amount",
            ],
        },
        {
            "pilot_name": "Quality Report Structure Templates",
            "business_problem": (
                "Quality reporting is inconsistent and time-consuming. The Quality Lead spends "
                "2–3 days compiling evidence pre-inspection."
            ),
            "proposed_solution": (
                "AI-generate report structure templates for common quality reports (observation "
                "feedback, self-assessment, inspection evidence summaries). Staff populate content; "
                "AI does not handle confidential learner or performance data."
            ),
            "expected_benefits": [
                "Reduce pre-inspection evidence compilation time by 30–40%",
                "Improve consistency of quality report formatting",
                "Create reusable report templates for future cycles",
            ],
            "complexity": "Medium",
            "risk_level": "Medium",
            "suggested_timeline": "Month 2–3",
            "success_measures": [
                "At least 3 quality report templates created and approved",
                "No confidential learner or staff data entered into AI tools",
                "Quality Lead time saving measurable in next inspection cycle",
            ],
        },
    ]


def get_demo_training_needs() -> list:
    """Return synthetic training needs for BrightPath."""
    return [
        {
            "topic": "Responsible AI Use Policy Awareness",
            "audience": "All staff",
            "priority": "High",
            "reason": (
                "No AI policy currently exists. All staff need to understand the boundaries "
                "before AI use continues."
            ),
            "recommended_format": "All-staff briefing (1 hour) + one-page reference guide",
        },
        {
            "topic": "Data Protection and AI Tools",
            "audience": "All staff",
            "priority": "High",
            "reason": (
                "Risk of learner and personal data entering AI tools without GDPR controls. "
                "Critical training before AI pilots launch."
            ),
            "recommended_format": "Online module (30 minutes) + knowledge check",
        },
        {
            "topic": "AI-Assisted Lesson Planning",
            "audience": "Curriculum and Learning Design team",
            "priority": "High",
            "reason": (
                "This team will be the first to pilot AI-assisted content creation. "
                "They need practical skills and responsible-use guidance."
            ),
            "recommended_format": "Half-day workshop with hands-on practice (Build 4 prototype)",
        },
        {
            "topic": "Spotting AI Hallucinations",
            "audience": "Tutors and Curriculum Lead",
            "priority": "Medium",
            "reason": (
                "All staff producing learner-facing content need to recognise and verify "
                "AI-generated factual claims."
            ),
            "recommended_format": "Practical workshop (2 hours) with real hallucination examples",
        },
        {
            "topic": "Safeguarding and AI Boundaries",
            "audience": "All staff",
            "priority": "High",
            "reason": (
                "Explicit prohibition of AI in any safeguarding context must be communicated "
                "clearly and documented."
            ),
            "recommended_format": (
                "Safeguarding lead briefing (30 minutes) + written policy acknowledgement"
            ),
        },
        {
            "topic": "AI for Administration — Email and Document Templates",
            "audience": "Administration and Operations team",
            "priority": "Medium",
            "reason": (
                "Admin team will use AI for email templates and document drafting. "
                "Needs practical guidance on safe use and data boundaries."
            ),
            "recommended_format": "Team workshop (2 hours) with template creation exercise",
        },
    ]


def get_demo_governance_gaps() -> list:
    """Return synthetic governance gaps for BrightPath."""
    return [
        {
            "gap_title": "No AI Use Policy",
            "current_state": "No formal policy exists. AI use is informal and ungoverned.",
            "why_it_matters": (
                "Without a policy, there is no legal basis for controlling how staff use AI tools, "
                "no data protection safeguard, and no accountability framework."
            ),
            "recommended_action": (
                "Draft and approve an AI Use Policy covering: approved tools, prohibited uses, "
                "data boundaries, human review requirements, safeguarding restrictions, and "
                "responsible-owner sign-off."
            ),
            "priority": "Critical",
        },
        {
            "gap_title": "No Approved Tools List",
            "current_state": (
                "Staff are using personal ChatGPT accounts and other unapproved tools "
                "without organisational data agreements."
            ),
            "why_it_matters": (
                "Personal accounts do not carry organisational data processing agreements. "
                "Data entered may be used for model training and is outside GDPR controls."
            ),
            "recommended_action": (
                "Establish an approved tools list. Negotiate a business-tier account for ChatGPT "
                "or equivalent with a Data Processing Agreement."
            ),
            "priority": "Critical",
        },
        {
            "gap_title": "No Data Processing Agreement for AI Tools",
            "current_state": "No DPA or DPIA exists for any AI tool in use.",
            "why_it_matters": (
                "GDPR requires a Data Processing Agreement and potentially a Data Protection "
                "Impact Assessment before processing personal data through a third-party tool."
            ),
            "recommended_action": (
                "Complete a DPIA for any AI tool that may touch learner or staff data. "
                "Obtain DPAs with approved tool providers before piloting."
            ),
            "priority": "High",
        },
        {
            "gap_title": "No AI Output Review Process",
            "current_state": "No formal review process exists for AI-generated content before it reaches learners.",
            "why_it_matters": (
                "AI-generated content may contain errors, hallucinations, or inappropriate language. "
                "Without review, this reaches learners unchecked."
            ),
            "recommended_action": (
                "Define a mandatory review and sign-off process for all AI-generated content "
                "before learner delivery. Include in AI policy."
            ),
            "priority": "High",
        },
        {
            "gap_title": "No AI Use Log or Audit Trail",
            "current_state": "AI use is not logged or tracked in any way.",
            "why_it_matters": (
                "For Ofsted and internal governance, evidence of responsible AI use may be required. "
                "An absence of records creates compliance risk."
            ),
            "recommended_action": (
                "Introduce a simple AI use log: tool used, purpose, review completed by, date. "
                "Can be a spreadsheet initially."
            ),
            "priority": "Medium",
        },
    ]
