"""Deterministic synthetic delivery data for Build 8 Phase 1.

Every organisation, action, workflow, owner role, blocker, and check-in in
this module is fictional portfolio data. No real client or personal data is
used.
"""


def get_synthetic_delivery_organisations() -> list[dict]:
    """Return fictional organisations for the delivery tracker."""
    return [
        {
            "organisation_id": "ORG001",
            "organisation_name": "BrightPath Skills Training",
            "sector": "Adult skills training",
            "staff_count": 8,
            "implementation_stage": "Pilot follow-up",
        },
        {
            "organisation_id": "ORG002",
            "organisation_name": "Northside Community Advice",
            "sector": "Charity / advice service",
            "staff_count": 14,
            "implementation_stage": "Controlled rollout",
        },
        {
            "organisation_id": "ORG003",
            "organisation_name": "Greenacre Dental Group",
            "sector": "Healthcare administration",
            "staff_count": 22,
            "implementation_stage": "Governance-led pilot",
        },
    ]


def get_synthetic_implementation_actions() -> list[dict]:
    """Return fictional implementation actions linked to Builds 1, 4, 5, 6, and 7."""
    return [
        {
            "action_id": "ACT001",
            "organisation_id": "ORG001",
            "organisation_name": "BrightPath Skills Training",
            "workflow_id": "WF001",
            "workflow_name": "Lesson plan drafting",
            "related_build": "Build 4",
            "action_title": "Create lesson plan review checklist",
            "action_description": (
                "Create a simple checklist for tutors to review AI-assisted lesson "
                "plan drafts before use."
            ),
            "owner_role": "Training Lead",
            "priority": "High",
            "status": "In progress",
            "due_in_days": 14,
            "blocker": "Checklist criteria need agreement",
            "governance_signoff_required": False,
            "training_followup_required": True,
            "client_checkin_required": True,
            "evidence_note": (
                "Tutors saved time but quality review still needs to be standardised."
            ),
        },
        {
            "action_id": "ACT002",
            "organisation_id": "ORG001",
            "organisation_name": "BrightPath Skills Training",
            "workflow_id": "WF002",
            "workflow_name": "Staff AI confidence check-in",
            "related_build": "Build 4",
            "action_title": "Complete tutor confidence refresher",
            "action_description": (
                "Deliver a short refresher on safe prompting, checking outputs, "
                "and escalating uncertain results."
            ),
            "owner_role": "Learning and Development Lead",
            "priority": "Medium",
            "status": "Completed",
            "due_in_days": 0,
            "blocker": "",
            "governance_signoff_required": False,
            "training_followup_required": True,
            "client_checkin_required": False,
            "evidence_note": (
                "Confidence improved after the first workshop, with a small gap remaining."
            ),
        },
        {
            "action_id": "ACT003",
            "organisation_id": "ORG001",
            "organisation_name": "BrightPath Skills Training",
            "workflow_id": "WF003",
            "workflow_name": "Workflow readiness review",
            "related_build": "Build 1",
            "action_title": "Confirm next workflow for controlled testing",
            "action_description": (
                "Review the readiness audit shortlist and agree which low-risk "
                "administrative workflow should enter the next pilot."
            ),
            "owner_role": "Operations Lead",
            "priority": "Medium",
            "status": "Not started",
            "due_in_days": 21,
            "blocker": "Leadership meeting not yet scheduled",
            "governance_signoff_required": False,
            "training_followup_required": False,
            "client_checkin_required": True,
            "evidence_note": (
                "The readiness review identified two viable workflows but no owner decision."
            ),
        },
        {
            "action_id": "ACT004",
            "organisation_id": "ORG001",
            "organisation_name": "BrightPath Skills Training",
            "workflow_id": "WF004",
            "workflow_name": "Governance policy checklist review",
            "related_build": "Build 6",
            "action_title": "Approve escalation wording",
            "action_description": (
                "Agree the escalation language used when tutors identify unsafe, "
                "unreliable, or inappropriate AI output."
            ),
            "owner_role": "Quality Lead",
            "priority": "High",
            "status": "Blocked",
            "due_in_days": 7,
            "blocker": "Responsible owner has not approved the escalation route",
            "governance_signoff_required": True,
            "training_followup_required": False,
            "client_checkin_required": True,
            "evidence_note": (
                "Build 7 recorded a risk incident and two near misses for this workflow."
            ),
        },
        {
            "action_id": "ACT005",
            "organisation_id": "ORG001",
            "organisation_name": "BrightPath Skills Training",
            "workflow_id": "WF001",
            "workflow_name": "Lesson plan drafting",
            "related_build": "Build 7",
            "action_title": "Record the first monthly adoption baseline",
            "action_description": (
                "Document time saved, quality checks, staff confidence, and review "
                "outcomes for the first completed pilot month."
            ),
            "owner_role": "Operations Lead",
            "priority": "Medium",
            "status": "Completed",
            "due_in_days": 0,
            "blocker": "",
            "governance_signoff_required": False,
            "training_followup_required": True,
            "client_checkin_required": False,
            "evidence_note": (
                "The first evidence period supports continuing with stronger review controls."
            ),
        },
        {
            "action_id": "ACT006",
            "organisation_id": "ORG002",
            "organisation_name": "Northside Community Advice",
            "workflow_id": "WF005",
            "workflow_name": "Advice triage workflow mapping",
            "related_build": "Build 1",
            "action_title": "Define the permitted triage mapping boundary",
            "action_description": (
                "Document which internal process-mapping tasks are permitted and "
                "which advice decisions must remain entirely human-led."
            ),
            "owner_role": "Service Manager",
            "priority": "High",
            "status": "In progress",
            "due_in_days": 10,
            "blocker": "Boundary wording needs trustee review",
            "governance_signoff_required": True,
            "training_followup_required": False,
            "client_checkin_required": True,
            "evidence_note": (
                "Workflow mapping was useful, but advice-specific boundaries need to be explicit."
            ),
        },
        {
            "action_id": "ACT007",
            "organisation_id": "ORG002",
            "organisation_name": "Northside Community Advice",
            "workflow_id": "WF007",
            "workflow_name": "Volunteer training refresher planning",
            "related_build": "Build 4",
            "action_title": "Schedule volunteer coordinator coaching",
            "action_description": (
                "Plan a coaching session on reviewing AI-assisted training outlines "
                "before they are used with volunteers."
            ),
            "owner_role": "Volunteer Coordinator",
            "priority": "Low",
            "status": "Deferred",
            "due_in_days": 35,
            "blocker": "Coordinator capacity is committed to seasonal induction",
            "governance_signoff_required": False,
            "training_followup_required": True,
            "client_checkin_required": False,
            "evidence_note": (
                "The workflow can continue under manager approval until coaching is rescheduled."
            ),
        },
        {
            "action_id": "ACT008",
            "organisation_id": "ORG002",
            "organisation_name": "Northside Community Advice",
            "workflow_id": "WF006",
            "workflow_name": "Draft service improvement report",
            "related_build": "Build 5",
            "action_title": "Introduce a sensitive-content red-flag check",
            "action_description": (
                "Add a pre-circulation check that prevents sensitive case details "
                "from entering AI-assisted report drafting."
            ),
            "owner_role": "Reporting Lead",
            "priority": "Medium",
            "status": "Not started",
            "due_in_days": 12,
            "blocker": "Red-flag examples need service manager input",
            "governance_signoff_required": False,
            "training_followup_required": True,
            "client_checkin_required": True,
            "evidence_note": (
                "Drafting saved time, but Build 7 identified quality and boundary concerns."
            ),
        },
        {
            "action_id": "ACT009",
            "organisation_id": "ORG002",
            "organisation_name": "Northside Community Advice",
            "workflow_id": "WF008",
            "workflow_name": "AI acceptable use policy review",
            "related_build": "Build 6",
            "action_title": "Resolve policy boundary before restart",
            "action_description": (
                "Complete a trustee-led review of prohibited data and advice uses "
                "before the paused policy workflow can restart."
            ),
            "owner_role": "Governance Trustee",
            "priority": "Critical",
            "status": "Blocked",
            "due_in_days": 5,
            "blocker": "Trustee sign-off meeting is pending",
            "governance_signoff_required": True,
            "training_followup_required": False,
            "client_checkin_required": True,
            "evidence_note": (
                "The workflow was stopped after unclear advice-sector boundaries were identified."
            ),
        },
        {
            "action_id": "ACT010",
            "organisation_id": "ORG002",
            "organisation_name": "Northside Community Advice",
            "workflow_id": "WF006",
            "workflow_name": "Draft service improvement report",
            "related_build": "Build 7",
            "action_title": "Agree evidence needed for continuation",
            "action_description": (
                "Set the quality, incident, and human-review evidence threshold "
                "required before report drafting can continue more widely."
            ),
            "owner_role": "Service Director",
            "priority": "High",
            "status": "In progress",
            "due_in_days": 18,
            "blocker": "Quality threshold has not been agreed",
            "governance_signoff_required": True,
            "training_followup_required": False,
            "client_checkin_required": False,
            "evidence_note": (
                "Build 7 recommended review rather than immediate scale or stop."
            ),
        },
        {
            "action_id": "ACT011",
            "organisation_id": "ORG003",
            "organisation_name": "Greenacre Dental Group",
            "workflow_id": "WF011",
            "workflow_name": "Clinical admin AI boundary training",
            "related_build": "Build 4",
            "action_title": "Add AI boundaries to new starter induction",
            "action_description": (
                "Embed the approved administrative AI boundaries and human-review "
                "rules into the new starter induction checklist."
            ),
            "owner_role": "Training Lead",
            "priority": "Medium",
            "status": "Completed",
            "due_in_days": 0,
            "blocker": "",
            "governance_signoff_required": False,
            "training_followup_required": True,
            "client_checkin_required": False,
            "evidence_note": (
                "Training completion and confidence supported scaling the refresher."
            ),
        },
        {
            "action_id": "ACT012",
            "organisation_id": "ORG003",
            "organisation_name": "Greenacre Dental Group",
            "workflow_id": "WF010",
            "workflow_name": "Recall letter drafting",
            "related_build": "Build 5",
            "action_title": "Review external letter approval workflow",
            "action_description": (
                "Check whether the named human approver process remains practical "
                "before increasing the number of AI-assisted recall drafts."
            ),
            "owner_role": "Practice Administrator",
            "priority": "Low",
            "status": "Deferred",
            "due_in_days": 28,
            "blocker": "Review moved to the next practice meeting",
            "governance_signoff_required": False,
            "training_followup_required": False,
            "client_checkin_required": True,
            "evidence_note": (
                "Drafting is faster, but every patient-facing letter still requires approval."
            ),
        },
        {
            "action_id": "ACT013",
            "organisation_id": "ORG003",
            "organisation_name": "Greenacre Dental Group",
            "workflow_id": "WF009",
            "workflow_name": "Appointment admin workflow audit",
            "related_build": "Build 1",
            "action_title": "Extend audit template to one new admin workflow",
            "action_description": (
                "Apply the proven workflow audit template to one additional "
                "low-risk administrative process under controlled monitoring."
            ),
            "owner_role": "Practice Manager",
            "priority": "High",
            "status": "In progress",
            "due_in_days": 16,
            "blocker": "",
            "governance_signoff_required": False,
            "training_followup_required": True,
            "client_checkin_required": False,
            "evidence_note": (
                "The appointment audit produced strong time-saving and confidence evidence."
            ),
        },
        {
            "action_id": "ACT014",
            "organisation_id": "ORG003",
            "organisation_name": "Greenacre Dental Group",
            "workflow_id": "WF012",
            "workflow_name": "Governance incident log review",
            "related_build": "Build 6",
            "action_title": "Approve quarterly near-miss review cadence",
            "action_description": (
                "Confirm the responsible owner, evidence fields, and quarterly "
                "review cadence for AI-related near misses."
            ),
            "owner_role": "Practice Manager",
            "priority": "Medium",
            "status": "Not started",
            "due_in_days": 20,
            "blocker": "Governance owner availability is unconfirmed",
            "governance_signoff_required": True,
            "training_followup_required": False,
            "client_checkin_required": True,
            "evidence_note": (
                "Near misses can be grouped consistently, but the review cadence is informal."
            ),
        },
        {
            "action_id": "ACT015",
            "organisation_id": "ORG003",
            "organisation_name": "Greenacre Dental Group",
            "workflow_id": "WF009",
            "workflow_name": "Appointment admin workflow audit",
            "related_build": "Build 7",
            "action_title": "Close first-month scale evidence review",
            "action_description": (
                "Record the approved scale decision, monitoring owner, and evidence "
                "review date for the appointment administration workflow."
            ),
            "owner_role": "Operations Coordinator",
            "priority": "Low",
            "status": "Completed",
            "due_in_days": 0,
            "blocker": "",
            "governance_signoff_required": False,
            "training_followup_required": False,
            "client_checkin_required": False,
            "evidence_note": (
                "Build 7 found the workflow ready to scale with continued monitoring."
            ),
        },
    ]


def get_synthetic_client_checkins() -> list[dict]:
    """Return fictional client check-ins linked to delivery follow-up."""
    return [
        {
            "checkin_id": "CHK001",
            "organisation_id": "ORG001",
            "checkin_period": "Week 2",
            "checkin_focus": "Training follow-up",
            "summary": (
                "Tutors are using AI more consistently but still need clearer "
                "review guidance."
            ),
            "next_review_focus": "Check whether the review checklist is being used.",
        },
        {
            "checkin_id": "CHK002",
            "organisation_id": "ORG001",
            "checkin_period": "Week 4",
            "checkin_focus": "Governance control",
            "summary": (
                "The escalation wording remains unresolved and is delaying wider pilot use."
            ),
            "next_review_focus": "Confirm the responsible owner and approval date.",
        },
        {
            "checkin_id": "CHK003",
            "organisation_id": "ORG002",
            "checkin_period": "Week 2",
            "checkin_focus": "Controlled rollout",
            "summary": (
                "Internal workflow mapping is useful, but staff need a clearer boundary "
                "between process support and advice decisions."
            ),
            "next_review_focus": "Review the permitted-use boundary with trustees.",
        },
        {
            "checkin_id": "CHK004",
            "organisation_id": "ORG002",
            "checkin_period": "Week 4",
            "checkin_focus": "Paused governance action",
            "summary": (
                "The acceptable-use policy workflow remains stopped while advice-sector "
                "data boundaries are reviewed."
            ),
            "next_review_focus": "Confirm whether trustee sign-off conditions are met.",
        },
        {
            "checkin_id": "CHK005",
            "organisation_id": "ORG003",
            "checkin_period": "Week 2",
            "checkin_focus": "Scale preparation",
            "summary": (
                "The appointment administration audit is ready to extend to one "
                "additional low-risk workflow."
            ),
            "next_review_focus": "Check the new workflow owner and monitoring measures.",
        },
        {
            "checkin_id": "CHK006",
            "organisation_id": "ORG003",
            "checkin_period": "Week 4",
            "checkin_focus": "Near-miss governance",
            "summary": (
                "Near-miss themes are being captured consistently, but the quarterly "
                "review cadence is not yet approved."
            ),
            "next_review_focus": "Confirm governance ownership and the first review date.",
        },
    ]
