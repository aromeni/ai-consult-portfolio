"""AI Staff Training and Workshop Generator — Streamlit app.

Build 4 of the BrightPath ChatGPT Mastery Project.
Phase 1: scaffold, synthetic scenario setup, and app navigation.
"""

import streamlit as st

from src import (
    sample_data,
    scenario_manager,
    needs_assessment as na,
    workshop_planner as wp,
    activity_generator as ag,
    facilitator_guide as fg,
    handout_generator as hg,
    knowledge_check as kc,
    training_pack as tp,
    report_analytics as ra,
    export_utils as eu,
    pdf_exporter as pe,
    pptx_exporter as ppt,
    ui_components as ui,
)

st.set_page_config(
    page_title="AI Staff Training Generator",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded",
)

ui.apply_global_styles()


def _generate_report_pdf(markdown_text: str, report_title: str, scenario: dict):
    """Generate a report PDF from its Markdown; returns (bytes | None, filename)."""
    org = scenario.get("organisation_name", "") if isinstance(scenario, dict) else ""
    filename = pe.create_safe_filename(f"{report_title} {org}".strip(), "pdf")
    try:
        pdf_bytes = pe.export_markdown_report_to_pdf_bytes(
            markdown_text,
            report_title=report_title,
            organisation_name=org,
            subtitle="Responsible AI staff training — synthetic scenario prototype",
        )
        return pdf_bytes, filename
    except Exception:
        return None, filename


def _render_report_downloads(
    md_text: str,
    md_filename: str,
    md_label: str,
    pdf_bytes_key: str,
    pdf_filename_key: str,
    pdf_label: str,
) -> None:
    """Render the standard Markdown + PDF download panel for a report page."""
    ui.render_export_panel("Download This Report")
    col_md, col_pdf = st.columns(2)
    with col_md:
        if md_text:
            st.download_button(
                label=md_label,
                data=md_text,
                file_name=md_filename,
                mime="text/markdown",
                use_container_width=True,
            )
    with col_pdf:
        pdf_bytes = st.session_state.get(pdf_bytes_key)
        if pdf_bytes:
            st.download_button(
                label=pdf_label,
                data=pdf_bytes,
                file_name=st.session_state.get(pdf_filename_key, "report.pdf"),
                mime="application/pdf",
                use_container_width=True,
            )
        else:
            st.caption("PDF not available for this session — regenerate the report to retry.")


# ── Sidebar navigation ─────────────────────────────────────────────────────────

PAGES = [
    "Home",
    "Organisation Scenario",
    "Training Needs Assessment",
    "Workshop Planner",
    "Activity Generator",
    "Facilitator Guide",
    "Staff Handout",
    "Knowledge Check",
    "Training Pack Export",
]

with st.sidebar:
    st.markdown("### AI Staff Training Generator")
    st.caption("Build 4 · Production-style prototype")
    st.divider()
    page = st.radio("Navigate", PAGES, label_visibility="collapsed")
    st.divider()

    st.markdown("**Workflow Status**")
    _workflow_status = [
        ("1. Scenario", "training_scenario"),
        ("2. Needs", "training_needs_assessment"),
        ("3. Workshop", "workshop_plan"),
        ("4. Activities", "training_activities"),
        ("5. Facilitator", "facilitator_guide"),
        ("6. Handout", "staff_handout"),
        ("7. Knowledge Check", "knowledge_check"),
        ("8. Training Pack", "training_pack_data"),
    ]
    for _label, _key in _workflow_status:
        if st.session_state.get(_key):
            st.markdown(
                f"<span class='wf-done'>✓ {_label}</span>",
                unsafe_allow_html=True,
            )
        else:
            st.markdown(
                f"<span class='wf-todo'>○ {_label}</span>",
                unsafe_allow_html=True,
            )
    st.divider()
    st.caption(
        "⚠ Synthetic scenarios only. No real learner, safeguarding, HR, "
        "confidential, personal, or regulated data."
    )


# ── Home ───────────────────────────────────────────────────────────────────────

if page == "Home":
    ui.render_page_header(
        "AI Staff Training and Workshop Generator",
        "Build 4 · BrightPath ChatGPT Mastery Project",
    )

    st.markdown(
        "A locally-run prototype that helps consultants and trainers turn AI adoption "
        "concerns into practical, responsible staff training materials — using synthetic "
        "organisation scenarios and deterministic generation."
    )

    st.markdown("---")

    st.markdown("### Consulting Workflow")
    st.markdown(
        "Work through the pages in order to generate a complete training pack:"
    )

    workflow_steps = [
        ("1", "Organisation Scenario", "Define the organisation, staff, concerns, and training goals"),
        ("2", "Training Needs Assessment", "Identify priority topics and risk themes"),
        ("3", "Workshop Planner", "Generate a structured agenda with timed segments and learning outcomes"),
        ("4", "Activity Generator", "Create practical activities: safe/unsafe prompts, scenario discussions, hallucination review"),
        ("5", "Facilitator Guide", "Generate trainer notes, discussion prompts, and debrief guidance"),
        ("6", "Staff Handout", "Create a staff-facing AI safe-use reference handout"),
        ("7", "Knowledge Check", "Generate quiz questions, scenario questions, and an answer key"),
        ("8", "Training Pack Export", "Combine all outputs into a downloadable Markdown training pack"),
    ]

    cols = st.columns(4)
    for i, (num, step_title, desc) in enumerate(workflow_steps):
        with cols[i % 4]:
            st.markdown(f"**{num}. {step_title}**")
            st.caption(desc)

    st.markdown("---")

    st.markdown("### How This Connects to Builds 1, 2, and 3")

    col1, col2 = st.columns(2)
    with col1:
        st.markdown(
            "**Build 1 — AI Readiness Audit**  \n"
            "Diagnosed where an organisation stands with AI: workflow gaps, "
            "risk areas, and staff readiness. The audit report identifies training needs "
            "that Build 4 turns into actionable materials."
        )
        st.markdown(
            "**Build 2 — Document Intelligence**  \n"
            "Extracted evidence from policy documents using keyword search. "
            "Build 4 can use policy document analysis to ground training materials "
            "in the organisation's actual policies."
        )
    with col2:
        st.markdown(
            "**Build 3 — Semantic RAG Policy Assistant**  \n"
            "Retrieved semantically relevant policy chunks and generated grounded answers. "
            "Build 4 can be extended to pull policy evidence from Build 3's RAG pipeline "
            "to support training content generation."
        )
        st.markdown(
            "**Build 4 — AI Staff Training Generator** *(this build)*  \n"
            "Closes the consulting loop: Audit → Document Intelligence → "
            "Semantic RAG → **Staff Training**. "
            "Turns AI adoption concerns into structured, responsible training materials."
        )

    st.markdown("---")

    ui.render_responsible_use_warning()

    st.markdown("---")

    ui.render_prototype_notice()


# ── Organisation Scenario ──────────────────────────────────────────────────────

elif page == "Organisation Scenario":
    ui.render_page_header(
        "Organisation Scenario",
        "Define the organisation, staff concerns, and training goals.",
    )

    ui.render_responsible_use_warning()

    st.markdown("---")

    # Load demo scenario
    st.markdown("#### Load Demo Scenario")
    st.markdown(
        "Load the BrightPath Skills Training synthetic demo scenario to explore "
        "the app. This is a fictional organisation — no real data."
    )

    if st.button("Load BrightPath Demo Scenario", type="primary"):
        scenario = sample_data.get_brightpath_training_scenario()
        st.session_state["training_scenario"] = scenario
        st.session_state["scenario_summary"] = scenario_manager.summarise_training_scenario(scenario)
        st.success("BrightPath demo scenario loaded.")
        st.rerun()

    st.markdown("---")

    # Scenario form
    st.markdown("#### Create or Edit Scenario")

    default = st.session_state.get(
        "training_scenario", sample_data.get_brightpath_training_scenario()
    )

    with st.form("scenario_form"):
        col1, col2 = st.columns(2)

        with col1:
            org_name = st.text_input("Organisation name", value=default.get("organisation_name", ""))
            org_type = st.text_input("Organisation type", value=default.get("organisation_type", ""))
            staff_count = st.number_input(
                "Staff count", min_value=1, max_value=10000,
                value=int(default.get("staff_count", 8))
            )
            sector = st.text_input("Sector", value=default.get("sector", ""))
            country = st.text_input("Country context", value=default.get("country_context", ""))

        with col2:
            training_duration = st.text_input("Training duration", value=default.get("training_duration", ""))
            delivery_mode = st.text_input("Delivery mode", value=default.get("delivery_mode", ""))

        current_ai_use = st.text_area(
            "Current AI use",
            value=default.get("current_ai_use", ""),
            height=80,
        )
        training_goal = st.text_area(
            "Training goal",
            value=default.get("training_goal", ""),
            height=80,
        )

        all_topics = sample_data.get_default_priority_topics()
        selected_topics = st.multiselect(
            "Priority topics",
            options=all_topics,
            default=[t for t in default.get("priority_topics", []) if t in all_topics],
        )

        all_roles = sample_data.get_default_staff_roles()
        selected_roles = st.multiselect(
            "Staff roles",
            options=all_roles,
            default=[r for r in default.get("staff_roles", []) if r in all_roles],
        )

        main_concerns_raw = st.text_area(
            "Main concerns (one per line)",
            value="\n".join(default.get("main_concerns", [])),
            height=100,
        )

        submitted = st.form_submit_button("Save Scenario", type="primary")

    if submitted:
        form_data = {
            "organisation_name": org_name,
            "organisation_type": org_type,
            "staff_count": staff_count,
            "sector": sector,
            "country_context": country,
            "current_ai_use": current_ai_use,
            "training_goal": training_goal,
            "training_duration": training_duration,
            "delivery_mode": delivery_mode,
            "priority_topics": selected_topics,
            "staff_roles": selected_roles,
            "main_concerns": main_concerns_raw,
        }
        scenario = scenario_manager.create_scenario_from_form_data(form_data)
        valid, msg = scenario_manager.validate_training_scenario(scenario)
        if valid:
            st.session_state["training_scenario"] = scenario
            st.session_state["scenario_summary"] = scenario_manager.summarise_training_scenario(scenario)
            st.success(msg)
            st.rerun()
        else:
            st.error(f"Scenario validation failed: {msg}")

    # Scenario summary and preview
    if "scenario_summary" in st.session_state:
        st.markdown("---")
        st.markdown("#### Scenario Summary")

        summary = st.session_state["scenario_summary"]
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Staff", summary["staff_count"])
        c2.metric("Priority topics", summary["topic_count"])
        c3.metric("Staff roles", summary["role_count"])
        c4.metric("Concerns", summary["concern_count"])

        col_a, col_b = st.columns(2)
        with col_a:
            st.markdown(f"**Organisation:** {summary['organisation_name']}")
            st.markdown(f"**Type:** {summary['organisation_type']}")
            st.markdown(f"**Sector:** {summary['sector']}")
        with col_b:
            st.markdown(f"**Country:** {summary['country_context']}")
            st.markdown(f"**Duration:** {summary['training_duration']}")
            st.markdown(f"**Delivery:** {summary['delivery_mode']}")

        st.markdown("---")
        st.markdown("#### Scenario Markdown Preview")
        with st.expander("View full scenario as Markdown"):
            md = scenario_manager.format_scenario_as_markdown(
                st.session_state["training_scenario"]
            )
            st.code(md, language="markdown")


# ── Placeholder pages ──────────────────────────────────────────────────────────

elif page == "Training Needs Assessment":
    ui.render_page_header(
        "Training Needs Assessment",
        "Analyse the saved scenario and identify priority topics, learning outcomes, and role-specific needs.",
    )
    ui.render_responsible_use_warning()
    st.markdown("---")

    if "training_scenario" not in st.session_state:
        st.warning("No scenario loaded. Complete these steps first:")
        st.markdown(
            "1. Go to **Organisation Scenario** in the sidebar.\n"
            "2. Click **Load BrightPath Demo Scenario** or fill in the form.\n"
            "3. Click **Save Scenario**.\n"
            "4. Return here to generate the Training Needs Assessment."
        )
    else:
        scenario = st.session_state["training_scenario"]
        summary = st.session_state.get("scenario_summary", {})

        # Scenario context
        st.markdown("#### Scenario")
        col_a, col_b, col_c = st.columns(3)
        col_a.markdown(f"**Organisation:** {scenario.get('organisation_name', '')}")
        col_b.markdown(f"**Staff count:** {scenario.get('staff_count', '')}")
        col_c.markdown(f"**Delivery:** {scenario.get('delivery_mode', '')}")

        st.markdown("---")

        if st.button("Generate Training Needs Assessment", type="primary"):
            with st.spinner("Analysing scenario..."):
                assessment = na.generate_training_needs_assessment(scenario)
                needs_md = na.format_needs_assessment_as_markdown(assessment)
                st.session_state["training_needs_assessment"] = assessment
                st.session_state["training_needs_markdown"] = needs_md
                pdf_bytes, pdf_filename = _generate_report_pdf(
                    needs_md, "Training Needs Assessment", scenario
                )
                st.session_state["training_needs_pdf_bytes"] = pdf_bytes
                st.session_state["training_needs_pdf_filename"] = pdf_filename
            st.success("Training needs assessment generated.")
            st.rerun()

        if "training_needs_assessment" in st.session_state:
            assessment = st.session_state["training_needs_assessment"]
            needs_summary = na.summarise_training_needs(assessment)

            st.markdown("---")
            st.markdown("#### Summary")

            c1, c2, c3, c4 = st.columns(4)
            c1.metric("Priority topics", needs_summary["priority_topic_count"])
            c2.metric("High priority", needs_summary["high_priority_count"])
            c3.metric("Staff roles", needs_summary["staff_role_count"])
            c4.metric("Learning outcomes", needs_summary["learning_outcome_count"])

            st.markdown(f"**Recommended session:** {needs_summary['recommended_session_type']}")
            st.markdown(f"**Overall focus:** {needs_summary['overall_training_focus']}")

            st.markdown("---")
            st.markdown("#### Topic Priorities")

            import pandas as pd
            topic_rows = [
                {
                    "Topic": t["title"],
                    "Priority": t["priority_level"].upper(),
                    "Risk": t["risk_level"].upper(),
                    "Training Need": t["training_need"][:120] + "…" if len(t["training_need"]) > 120 else t["training_need"],
                }
                for t in assessment.get("topic_assessments", [])
            ]
            if topic_rows:
                st.dataframe(pd.DataFrame(topic_rows), use_container_width=True, hide_index=True)

            st.markdown("---")
            st.markdown("#### Recommended Learning Outcomes")
            st.markdown("By the end of the training session, staff will be able to:")
            for outcome in assessment.get("recommended_learning_outcomes", []):
                st.markdown(f"- {outcome}")

            st.markdown("---")
            st.markdown("#### Role-Specific Training Needs")
            role_needs = assessment.get("role_specific_needs", [])
            if role_needs:
                for role_need in role_needs:
                    with st.expander(f"{role_need.get('role', 'Staff')}"):
                        st.markdown(f"**Training focus:** {role_need.get('training_focus', '')}")
                        risks = role_need.get("key_risks", [])
                        if risks:
                            st.markdown("**Key risks:**")
                            for risk in risks:
                                st.markdown(f"- {risk}")
                        guidance = role_need.get("practical_guidance", [])
                        if guidance:
                            st.markdown("**Practical guidance:**")
                            for g in guidance:
                                st.markdown(f"- {g}")

            st.markdown("---")
            st.markdown("#### Risk Summary")
            st.info(assessment.get("risk_summary", ""))

            st.markdown("---")
            st.markdown("#### Responsible Use")
            st.warning(assessment.get("responsible_use_note", ""), icon="⚠️")

            st.markdown("---")
            _render_report_downloads(
                md_text=st.session_state.get("training_needs_markdown", ""),
                md_filename=f"training-needs-assessment-{scenario.get('organisation_name', 'organisation').lower().replace(' ', '-')}.md",
                md_label="Download Training Needs Assessment (Markdown)",
                pdf_bytes_key="training_needs_pdf_bytes",
                pdf_filename_key="training_needs_pdf_filename",
                pdf_label="Download PDF Needs Assessment",
            )

elif page == "Workshop Planner":
    ui.render_page_header(
        "Workshop Planner",
        "Generate a structured responsible AI staff training session plan.",
    )
    ui.render_responsible_use_warning()
    st.markdown("---")

    if "training_scenario" not in st.session_state:
        st.warning("No scenario loaded. Complete these steps first:")
        st.markdown(
            "1. Go to **Organisation Scenario** in the sidebar.\n"
            "2. Click **Load BrightPath Demo Scenario** or fill in the form.\n"
            "3. Click **Save Scenario**.\n"
            "4. Return here to generate the Workshop Plan."
        )
    else:
        scenario = st.session_state["training_scenario"]
        assessment = st.session_state.get("training_needs_assessment")

        if assessment is None:
            st.info(
                "**Training Needs Assessment not yet run.** "
                "Go to Training Needs Assessment and generate it first for a more "
                "tailored workshop plan. A basic plan can still be generated from the scenario."
            )

        # Scenario context
        st.markdown("#### Scenario")
        col_a, col_b, col_c = st.columns(3)
        col_a.markdown(f"**Organisation:** {scenario.get('organisation_name', '')}")
        col_b.markdown(f"**Staff count:** {scenario.get('staff_count', '')}")
        col_c.markdown(f"**Priority topics:** {len(scenario.get('priority_topics', []))}")

        st.markdown("---")
        st.markdown("#### Workshop Settings")

        col_dur, col_mode = st.columns(2)
        with col_dur:
            duration_choice = st.selectbox(
                "Workshop duration",
                options=["60 minutes", "90 minutes", "120 minutes"],
                index=1,
            )
        with col_mode:
            mode_choice = st.selectbox(
                "Delivery mode",
                options=["In-person workshop", "Online workshop", "Hybrid workshop"],
                index=0,
            )

        duration_minutes = wp.normalise_duration_to_minutes(duration_choice)

        if st.button("Generate Workshop Plan", type="primary"):
            with st.spinner("Generating workshop plan..."):
                plan = wp.generate_workshop_plan(
                    scenario,
                    assessment=assessment,
                    duration_minutes=duration_minutes,
                    delivery_mode=mode_choice,
                )
                plan_md = wp.format_workshop_plan_as_markdown(plan)
                plan_filename = wp.create_workshop_plan_filename(plan["workshop_title"])
                st.session_state["workshop_plan"] = plan
                st.session_state["workshop_plan_markdown"] = plan_md
                st.session_state["workshop_plan_filename"] = plan_filename
                pdf_bytes, pdf_filename = _generate_report_pdf(
                    plan_md, "Workshop Plan", scenario
                )
                st.session_state["workshop_plan_pdf_bytes"] = pdf_bytes
                st.session_state["workshop_plan_pdf_filename"] = pdf_filename
            st.success("Workshop plan generated.")
            st.rerun()

        if "workshop_plan" in st.session_state:
            plan = st.session_state["workshop_plan"]
            plan_summary = wp.summarise_workshop_plan(plan)

            st.markdown("---")
            st.markdown("#### Summary")

            c1, c2, c3, c4 = st.columns(4)
            c1.metric("Duration", f"{plan_summary['duration_minutes']} min")
            c2.metric("Agenda sections", plan_summary["agenda_section_count"])
            c3.metric("Learning outcomes", plan_summary["learning_outcome_count"])
            c4.metric("Follow-up actions", plan_summary["follow_up_action_count"])

            st.markdown(f"**Workshop title:** {plan['workshop_title']}")
            st.markdown(f"**Audience:** {', '.join(plan.get('audience', []))}")
            st.markdown(f"**Delivery:** {plan.get('delivery_mode', '')}")

            st.markdown("---")
            st.markdown("#### Learning Outcomes")
            st.markdown("By the end of this session, staff will be able to:")
            for outcome in plan.get("learning_outcomes", []):
                st.markdown(f"- {outcome}")

            st.markdown("---")
            st.markdown("#### Timed Agenda")
            import pandas as pd
            agenda_rows = [
                {
                    "Time": item["time_range"],
                    "Section": item["section_title"],
                    "Purpose": item["purpose"][:90] + "…" if len(item["purpose"]) > 90 else item["purpose"],
                }
                for item in plan.get("agenda", [])
            ]
            if agenda_rows:
                st.dataframe(pd.DataFrame(agenda_rows), use_container_width=True, hide_index=True)

            st.markdown("---")
            st.markdown("#### Agenda Detail")
            for item in plan.get("agenda", []):
                with st.expander(f"{item['time_range']} — {item['section_title']}"):
                    st.markdown(f"**Purpose:** {item['purpose']}")
                    st.markdown(f"**Trainer activity:** {item['trainer_activity']}")
                    st.markdown(f"**Participant activity:** {item['participant_activity']}")
                    st.markdown(f"**Key message:** *{item['key_message']}*")
                    mats = item.get("materials", [])
                    if mats:
                        st.markdown("**Materials:** " + ", ".join(mats))

            st.markdown("---")
            st.markdown("#### Resources Needed")
            for resource in plan.get("resources_needed", []):
                st.markdown(f"- {resource}")

            st.markdown("---")
            st.markdown("#### Trainer Notes")
            for note in plan.get("trainer_notes", []):
                st.markdown(f"- {note}")

            st.markdown("---")
            st.markdown("#### Discussion Prompts")
            for i, prompt in enumerate(plan.get("discussion_prompts", []), 1):
                st.markdown(f"{i}. {prompt}")

            st.markdown("---")
            st.markdown("#### Responsible Use Messages")
            for msg in plan.get("responsible_use_messages", []):
                st.markdown(f"- {msg}")

            st.markdown("---")
            st.markdown("#### Follow-Up Actions")
            for action in plan.get("follow_up_actions", []):
                st.markdown(f"- {action}")

            st.markdown("---")
            _render_report_downloads(
                md_text=st.session_state.get("workshop_plan_markdown", ""),
                md_filename=st.session_state.get("workshop_plan_filename", "workshop-plan.md"),
                md_label="Download Workshop Plan (Markdown)",
                pdf_bytes_key="workshop_plan_pdf_bytes",
                pdf_filename_key="workshop_plan_pdf_filename",
                pdf_label="Download PDF Workshop Plan",
            )

elif page == "Activity Generator":
    ui.render_page_header(
        "Activity Generator",
        "Generate practical responsible AI workshop activities from the saved scenario.",
    )
    ui.render_responsible_use_warning()
    st.markdown("---")

    if "training_scenario" not in st.session_state:
        st.warning("No scenario loaded. Complete these steps first:")
        st.markdown(
            "1. Go to **Organisation Scenario** in the sidebar.\n"
            "2. Click **Load BrightPath Demo Scenario** or fill in the form.\n"
            "3. Click **Save Scenario**.\n"
            "4. Return here to generate activities."
        )
    else:
        scenario = st.session_state["training_scenario"]
        assessment = st.session_state.get("training_needs_assessment")
        workshop_plan = st.session_state.get("workshop_plan")

        if assessment is None or workshop_plan is None:
            st.info(
                "**Training Needs Assessment and/or Workshop Plan not yet run.** "
                "Go to those pages for more tailored activities. "
                "Basic activities can still be generated from the scenario."
            )

        # Scenario context
        st.markdown("#### Scenario")
        col_a, col_b, col_c = st.columns(3)
        col_a.markdown(f"**Organisation:** {scenario.get('organisation_name', '')}")
        col_b.markdown(f"**Staff count:** {scenario.get('staff_count', '')}")
        col_c.markdown(f"**Priority topics:** {len(scenario.get('priority_topics', []))}")

        st.markdown("---")
        st.markdown("#### Select Activities")

        catalogue = ag.get_activity_type_catalogue()
        catalogue_options = {
            activity_id: info["title"]
            for activity_id, info in catalogue.items()
        }
        default_selected = ag.get_default_activity_types()

        selected_ids = st.multiselect(
            "Choose which activities to generate",
            options=list(catalogue_options.keys()),
            default=default_selected,
            format_func=lambda x: catalogue_options.get(x, x),
        )

        if st.button("Generate Activities", type="primary"):
            if not selected_ids:
                st.error("Select at least one activity type.")
            else:
                with st.spinner("Generating activities..."):
                    activities = ag.generate_training_activities(
                        scenario,
                        assessment=assessment,
                        workshop_plan=workshop_plan,
                        selected_activity_types=selected_ids,
                    )
                    activities_md = ag.format_activities_as_markdown(activities)
                    activities_filename = ag.create_activities_filename(
                        scenario.get("organisation_name", "organisation")
                    )
                    st.session_state["training_activities"] = activities
                    st.session_state["training_activities_markdown"] = activities_md
                    st.session_state["training_activities_filename"] = activities_filename
                    pdf_bytes, pdf_filename = _generate_report_pdf(
                        activities_md, "Training Activity Pack", scenario
                    )
                    st.session_state["training_activities_pdf_bytes"] = pdf_bytes
                    st.session_state["training_activities_pdf_filename"] = pdf_filename
                st.success(f"{len(activities)} activities generated.")
                st.rerun()

        if "training_activities" in st.session_state:
            activities = st.session_state["training_activities"]
            act_summary = ag.summarise_training_activities(activities)

            st.markdown("---")
            st.markdown("#### Summary")

            c1, c2, c3, c4 = st.columns(4)
            c1.metric("Activities", act_summary["activity_count"])
            c2.metric("Est. time (min)", act_summary["estimated_total_minutes"])
            c3.metric("Activity types", len(act_summary["activity_types"]))
            c4.metric("Target roles", len(act_summary["target_roles"]))

            st.markdown("---")
            st.markdown("#### Activities")

            for i, activity in enumerate(activities, 1):
                title = activity.get("activity_title", "Activity")
                duration = activity.get("duration_minutes", "")
                with st.expander(f"Activity {i}: {title} ({duration} min)"):
                    col_x, col_y = st.columns(2)
                    col_x.markdown(f"**Type:** {activity.get('activity_type', '').capitalize()}")
                    col_y.markdown(f"**Duration:** {duration} minutes")

                    roles = activity.get("target_roles", [])
                    if roles:
                        st.markdown(f"**Target roles:** {', '.join(roles)}")

                    st.markdown(f"**Learning objective:** {activity.get('learning_objective', '')}")

                    materials = activity.get("materials_needed", [])
                    if materials:
                        st.markdown("**Materials needed:**")
                        for m in materials:
                            st.markdown(f"- {m}")

                    trainer_instrs = activity.get("instructions_for_trainer", [])
                    if trainer_instrs:
                        st.markdown("**Trainer instructions:**")
                        for j, instr in enumerate(trainer_instrs, 1):
                            st.markdown(f"{j}. {instr}")

                    participant_instrs = activity.get("instructions_for_participants", [])
                    if participant_instrs:
                        st.markdown("**Participant instructions:**")
                        for instr in participant_instrs:
                            st.markdown(f"- {instr}")

                    scenario_cards = activity.get("scenario_cards", [])
                    if scenario_cards:
                        st.markdown("**Scenario cards / examples:**")
                        for card in scenario_cards:
                            card_id = card.get("card_id", "")
                            if "prompt" in card:
                                st.markdown(
                                    f"*Card {card_id}:* \"{card['prompt']}\" "
                                    f"→ **{card.get('classification', '')}**"
                                )
                            elif "original_prompt" in card:
                                st.markdown(
                                    f"*Card {card_id} (original):* \"{card['original_prompt']}\""
                                )
                                st.markdown(
                                    f"*Safe rewrite:* \"{card.get('safe_rewrite', '')}\""
                                )
                            elif "situation" in card:
                                st.markdown(f"*Card {card_id}:* {card['situation']}")
                                if card.get("correct_action"):
                                    st.markdown(f"*Correct action:* {card['correct_action']}")
                            elif "proposed_use" in card:
                                st.markdown(
                                    f"*Card {card_id}:* {card['proposed_use']} "
                                    f"→ **{card.get('decision', '')}**"
                                )
                            elif "ai_output" in card:
                                st.markdown(f"*Card {card_id} (AI output):* \"{card['ai_output']}\"")
                            elif "task" in card:
                                st.markdown(f"*Card {card_id}:* {card['task']}")

                    expected = activity.get("expected_answers", [])
                    if expected:
                        st.markdown("**Expected answers:**")
                        for ans in expected:
                            st.markdown(f"- {ans}")

                    debrief = activity.get("debrief_questions", [])
                    if debrief:
                        st.markdown("**Debrief questions:**")
                        for j, q in enumerate(debrief, 1):
                            st.markdown(f"{j}. {q}")

                    takeaways = activity.get("key_takeaways", [])
                    if takeaways:
                        st.markdown("**Key takeaways:**")
                        for t in takeaways:
                            st.markdown(f"- {t}")

                    st.warning(
                        activity.get("responsible_use_note", ""), icon="⚠️"
                    )

            st.markdown("---")
            _render_report_downloads(
                md_text=st.session_state.get("training_activities_markdown", ""),
                md_filename=st.session_state.get("training_activities_filename", "training-activities.md"),
                md_label="Download Activities (Markdown)",
                pdf_bytes_key="training_activities_pdf_bytes",
                pdf_filename_key="training_activities_pdf_filename",
                pdf_label="Download PDF Activity Pack",
            )

elif page == "Facilitator Guide":
    ui.render_page_header(
        "Facilitator Guide",
        "Generate trainer-facing delivery notes, scripts, and activity guidance for the workshop.",
    )
    ui.render_responsible_use_warning()
    st.markdown("---")

    if "training_scenario" not in st.session_state:
        st.warning("No scenario loaded. Complete these steps first:")
        st.markdown(
            "1. Go to **Organisation Scenario** in the sidebar.\n"
            "2. Click **Load BrightPath Demo Scenario** or fill in the form.\n"
            "3. Click **Save Scenario**.\n"
            "4. Return here to generate the Facilitator Guide."
        )
    else:
        scenario = st.session_state["training_scenario"]
        assessment = st.session_state.get("training_needs_assessment")
        workshop_plan = st.session_state.get("workshop_plan")
        activities = st.session_state.get("training_activities")

        missing = []
        if assessment is None:
            missing.append("Training Needs Assessment")
        if workshop_plan is None:
            missing.append("Workshop Plan")
        if activities is None:
            missing.append("Training Activities")

        if missing:
            st.info(
                f"**{', '.join(missing)} not yet run.** "
                "Go to the earlier pages for a richer facilitator guide. "
                "A basic guide can still be generated from the scenario."
            )

        # Scenario context
        st.markdown("#### Scenario")
        col_a, col_b, col_c = st.columns(3)
        col_a.markdown(f"**Organisation:** {scenario.get('organisation_name', '')}")
        col_b.markdown(f"**Staff count:** {scenario.get('staff_count', '')}")
        col_c.markdown(f"**Delivery:** {scenario.get('delivery_mode', '')}")

        st.markdown("---")

        if st.button("Generate Facilitator Guide", type="primary"):
            with st.spinner("Generating facilitator guide..."):
                guide = fg.generate_facilitator_guide(
                    scenario,
                    assessment=assessment,
                    workshop_plan=workshop_plan,
                    activities=activities,
                )
                guide_md = fg.format_facilitator_guide_as_markdown(guide)
                guide_filename = fg.create_facilitator_guide_filename(
                    scenario.get("organisation_name", "organisation")
                )
                st.session_state["facilitator_guide"] = guide
                st.session_state["facilitator_guide_markdown"] = guide_md
                st.session_state["facilitator_guide_filename"] = guide_filename
                pdf_bytes, pdf_filename = _generate_report_pdf(
                    guide_md, "Facilitator Guide", scenario
                )
                st.session_state["facilitator_guide_pdf_bytes"] = pdf_bytes
                st.session_state["facilitator_guide_pdf_filename"] = pdf_filename
            st.success("Facilitator guide generated.")
            st.rerun()

        if "facilitator_guide" in st.session_state:
            guide = st.session_state["facilitator_guide"]
            guide_summary = fg.summarise_facilitator_guide(guide)

            st.markdown("---")
            st.markdown("#### Summary")

            c1, c2, c3, c4 = st.columns(4)
            c1.metric("Duration", f"{guide_summary['duration_minutes']} min")
            c2.metric("Sections", guide_summary["section_count"])
            c3.metric("Activities", guide_summary["activities_covered"])
            c4.metric("Misconceptions", guide_summary["misconception_count"])

            st.markdown(f"**Guide title:** {guide['guide_title']}")
            st.markdown(f"**Audience:** {', '.join(guide.get('audience', []))}")
            st.markdown(f"**Delivery:** {guide.get('delivery_mode', '')}")

            st.markdown("---")
            st.markdown("#### Session Purpose")
            st.info(guide.get("session_purpose", ""))

            st.markdown("---")
            st.markdown("#### Facilitator Principles")
            for principle in guide.get("facilitator_principles", []):
                st.markdown(f"- {principle}")

            st.markdown("---")
            st.markdown("#### Preparation Checklist")
            for i, item in enumerate(guide.get("preparation_checklist", []), 1):
                st.markdown(f"{i}. {item}")

            st.markdown("---")
            st.markdown("#### Opening Script")
            with st.expander("View opening script"):
                st.markdown(guide.get("opening_script", ""))

            st.markdown("---")
            st.markdown("#### Section-by-Section Delivery Notes")
            for note in guide.get("section_delivery_notes", []):
                with st.expander(note.get("section_title", "Section")):
                    if note.get("suggested_timing"):
                        st.markdown(f"**Timing:** {note['suggested_timing']}")
                    st.markdown(f"**Facilitator goal:** {note.get('facilitator_goal', '')}")
                    st.markdown(f"**What to say:** {note.get('what_to_say', '')}")
                    asks = note.get("what_to_ask", [])
                    if asks:
                        st.markdown("**What to ask:**")
                        for q in asks:
                            st.markdown(f"- {q}")
                    responses = note.get("expected_responses", [])
                    if responses:
                        st.markdown("**Expected responses:**")
                        for r in responses:
                            st.markdown(f"- {r}")
                    watch = note.get("watch_out_for", [])
                    if watch:
                        st.markdown("**Watch out for:**")
                        for w in watch:
                            st.markdown(f"- {w}")
                    if note.get("transition_note"):
                        st.markdown(f"**Transition:** {note['transition_note']}")

            st.markdown("---")
            st.markdown("#### Activity Facilitation Notes")
            for note in guide.get("activity_facilitation_notes", []):
                label = f"{note.get('activity_title', 'Activity')} ({note.get('duration_minutes', 10)} min)"
                with st.expander(label):
                    st.markdown(f"**Facilitator goal:** {note.get('facilitator_goal', '')}")
                    how = note.get("how_to_run", [])
                    if how:
                        st.markdown("**How to run:**")
                        for i, step in enumerate(how, 1):
                            st.markdown(f"{i}. {step}")
                    expected = note.get("expected_answers", [])
                    if expected:
                        st.markdown("**Expected answers:**")
                        for ans in expected:
                            st.markdown(f"- {ans}")
                    debrief = note.get("debrief_questions", [])
                    if debrief:
                        st.markdown("**Debrief questions:**")
                        for q in debrief:
                            st.markdown(f"- {q}")
                    takeaways = note.get("key_takeaways", [])
                    if takeaways:
                        st.markdown("**Key takeaways:**")
                        for t in takeaways:
                            st.markdown(f"- {t}")

            st.markdown("---")
            st.markdown("#### Common Misconceptions")
            for m in guide.get("common_misconceptions", []):
                with st.expander(f"Misconception: \"{m.get('misconception', '')}\""):
                    st.markdown(f"**Why it is risky:** {m.get('why_it_is_risky', '')}")
                    st.markdown(f"**Facilitator response:** {m.get('facilitator_response', '')}")

            st.markdown("---")
            st.markdown("#### Debrief Guidance")
            for i, item in enumerate(guide.get("debrief_guidance", []), 1):
                st.markdown(f"{i}. {item}")

            st.markdown("---")
            st.markdown("#### Risk Warnings")
            for warning in guide.get("risk_warnings", []):
                st.markdown(f"- {warning}")

            st.markdown("---")
            st.markdown("#### Closing Script")
            with st.expander("View closing script"):
                st.markdown(guide.get("closing_script", ""))

            st.markdown("---")
            _render_report_downloads(
                md_text=st.session_state.get("facilitator_guide_markdown", ""),
                md_filename=st.session_state.get("facilitator_guide_filename", "facilitator-guide.md"),
                md_label="Download Facilitator Guide (Markdown)",
                pdf_bytes_key="facilitator_guide_pdf_bytes",
                pdf_filename_key="facilitator_guide_pdf_filename",
                pdf_label="Download PDF Facilitator Guide",
            )

elif page == "Staff Handout":
    ui.render_page_header(
        "Staff Handout",
        "Generate a staff-facing responsible AI safe-use reference for the workshop.",
    )
    ui.render_responsible_use_warning()
    st.markdown("---")

    if "training_scenario" not in st.session_state:
        st.warning("No scenario loaded. Complete these steps first:")
        st.markdown(
            "1. Go to **Organisation Scenario** in the sidebar.\n"
            "2. Click **Load BrightPath Demo Scenario** or fill in the form.\n"
            "3. Click **Save Scenario**.\n"
            "4. Return here to generate the Staff Handout."
        )
    else:
        scenario = st.session_state["training_scenario"]
        assessment = st.session_state.get("training_needs_assessment")
        workshop_plan = st.session_state.get("workshop_plan")
        activities = st.session_state.get("training_activities")
        facilitator_guide_data = st.session_state.get("facilitator_guide")

        missing = []
        if assessment is None:
            missing.append("Training Needs Assessment")
        if workshop_plan is None:
            missing.append("Workshop Plan")
        if activities is None:
            missing.append("Training Activities")
        if facilitator_guide_data is None:
            missing.append("Facilitator Guide")

        if missing:
            st.info(
                f"**{', '.join(missing)} not yet run.** "
                "Go to the earlier pages for a richer handout. "
                "A basic handout can still be generated from the scenario."
            )

        # Scenario context
        st.markdown("#### Scenario")
        col_a, col_b, col_c = st.columns(3)
        col_a.markdown(f"**Organisation:** {scenario.get('organisation_name', '')}")
        col_b.markdown(f"**Staff count:** {scenario.get('staff_count', '')}")
        col_c.markdown(f"**Staff roles:** {len(scenario.get('staff_roles', []))}")

        st.markdown("---")

        if st.button("Generate Staff Handout", type="primary"):
            with st.spinner("Generating staff handout..."):
                handout = hg.generate_staff_handout(
                    scenario,
                    assessment=assessment,
                    workshop_plan=workshop_plan,
                    activities=activities,
                    facilitator_guide=facilitator_guide_data,
                )
                handout_md = hg.format_staff_handout_as_markdown(handout)
                handout_filename = hg.create_staff_handout_filename(
                    scenario.get("organisation_name", "organisation")
                )
                st.session_state["staff_handout"] = handout
                st.session_state["staff_handout_markdown"] = handout_md
                st.session_state["staff_handout_filename"] = handout_filename
                pdf_bytes, pdf_filename = _generate_report_pdf(
                    handout_md, "Staff Handout", scenario
                )
                st.session_state["staff_handout_pdf_bytes"] = pdf_bytes
                st.session_state["staff_handout_pdf_filename"] = pdf_filename
            st.success("Staff handout generated.")
            st.rerun()

        if "staff_handout" in st.session_state:
            handout = st.session_state["staff_handout"]
            handout_summary = hg.summarise_staff_handout(handout)

            st.markdown("---")
            st.markdown("#### Summary")

            c1, c2, c3, c4, c5 = st.columns(5)
            c1.metric("Organisation", handout_summary["organisation_name"])
            c2.metric("Audience roles", len(handout_summary["audience_roles"]))
            c3.metric("Safe prompt examples", handout_summary["safe_prompt_count"])
            c4.metric("Unsafe prompt examples", handout_summary["unsafe_prompt_count"])
            c5.metric("Escalation items", handout_summary["escalation_item_count"])

            st.markdown("---")
            st.markdown(f"#### {handout['handout_title']}")
            st.markdown(f"**Audience:** {', '.join(handout.get('audience', []))}")
            st.info(handout.get("purpose", ""))

            st.markdown("---")
            st.markdown("#### Safe-Use Principles")
            for principle in handout.get("safe_use_principles", []):
                st.markdown(f"- {principle}")

            st.markdown("---")
            st.markdown("#### What Staff Can Use AI For")
            for use in handout.get("allowed_ai_uses", []):
                st.markdown(f"- {use}")

            st.markdown("---")
            st.markdown("#### What Staff Must Not Use AI For")
            for use in handout.get("prohibited_ai_uses", []):
                st.markdown(f"- {use}")

            st.markdown("---")
            st.markdown("#### Safe Prompt Examples")
            for ex in handout.get("safe_prompt_examples", []):
                with st.expander(ex.get("title", "Example")):
                    st.markdown(f"**Prompt:** *{ex.get('prompt', '')}*")
                    st.markdown(f"**Why it is safe:** {ex.get('why_it_is_safe', '')}")

            st.markdown("---")
            st.markdown("#### Unsafe Prompt Examples")
            for ex in handout.get("unsafe_prompt_examples", []):
                with st.expander(ex.get("title", "Example")):
                    st.markdown(f"**Prompt:** *{ex.get('prompt', '')}*")
                    st.markdown(f"**Why it is risky:** {ex.get('why_it_is_risky', '')}")

            st.markdown("---")
            st.markdown("#### Safer Rewritten Prompt Examples")
            for i, ex in enumerate(handout.get("safer_rewritten_prompt_examples", []), 1):
                with st.expander(f"Example {i}"):
                    st.markdown(f"**Unsafe prompt:** *{ex.get('unsafe_prompt', '')}*")
                    st.markdown(f"**Safer prompt:** *{ex.get('safer_prompt', '')}*")
                    what_changed = ex.get("what_changed", [])
                    if what_changed:
                        st.markdown("**What changed:**")
                        for change in what_changed:
                            st.markdown(f"- {change}")

            st.markdown("---")
            st.markdown("#### Human Review Checklist")
            st.markdown("Before using any AI output, check:")
            for item in handout.get("human_review_checklist", []):
                st.markdown(f"- ☐ {item}")

            st.markdown("---")
            st.markdown("#### Escalation Guidance")
            for item in handout.get("escalation_guidance", []):
                with st.expander(item.get("issue", "Issue")):
                    st.markdown(f"**What to do:** {item.get('what_to_do', '')}")
                    st.markdown(f"**Who to contact:** {item.get('who_to_contact', '')}")

            st.markdown("---")
            st.markdown("#### Key Takeaways")
            for takeaway in handout.get("key_takeaways", []):
                st.markdown(f"- {takeaway}")

            st.markdown("---")
            st.warning(handout.get("responsible_use_warning", ""), icon="⚠️")

            st.markdown("---")
            _render_report_downloads(
                md_text=st.session_state.get("staff_handout_markdown", ""),
                md_filename=st.session_state.get("staff_handout_filename", "staff-handout.md"),
                md_label="Download Staff Handout (Markdown)",
                pdf_bytes_key="staff_handout_pdf_bytes",
                pdf_filename_key="staff_handout_pdf_filename",
                pdf_label="Download PDF Staff Handout",
            )

elif page == "Knowledge Check":
    ui.render_page_header(
        "Knowledge Check",
        "Generate responsible AI quiz questions, scenario questions, reflection prompts, and an answer key.",
    )
    ui.render_responsible_use_warning()
    st.markdown("---")

    if "training_scenario" not in st.session_state:
        st.warning("No scenario loaded. Complete these steps first:")
        st.markdown(
            "1. Go to **Organisation Scenario** in the sidebar.\n"
            "2. Click **Load BrightPath Demo Scenario** or fill in the form.\n"
            "3. Click **Save Scenario**.\n"
            "4. Return here to generate the Knowledge Check."
        )
    else:
        scenario = st.session_state["training_scenario"]
        assessment = st.session_state.get("training_needs_assessment")
        workshop_plan = st.session_state.get("workshop_plan")
        activities = st.session_state.get("training_activities")
        facilitator_guide_data = st.session_state.get("facilitator_guide")
        staff_handout = st.session_state.get("staff_handout")

        missing = []
        if assessment is None:
            missing.append("Training Needs Assessment")
        if workshop_plan is None:
            missing.append("Workshop Plan")
        if activities is None:
            missing.append("Training Activities")
        if facilitator_guide_data is None:
            missing.append("Facilitator Guide")
        if staff_handout is None:
            missing.append("Staff Handout")

        if missing:
            st.info(
                f"**{', '.join(missing)} not yet run.** "
                "Go to the earlier pages for a richer knowledge check. "
                "A basic knowledge check can still be generated from the scenario."
            )

        # Scenario context
        st.markdown("#### Scenario")
        col_a, col_b, col_c = st.columns(3)
        col_a.markdown(f"**Organisation:** {scenario.get('organisation_name', '')}")
        col_b.markdown(f"**Staff count:** {scenario.get('staff_count', '')}")
        col_c.markdown(f"**Staff roles:** {len(scenario.get('staff_roles', []))}")

        st.markdown("---")
        st.markdown("#### Knowledge Check Settings")

        col_count, col_gap = st.columns([1, 2])
        with col_count:
            question_count_choice = st.selectbox(
                "Number of multiple-choice questions",
                options=[5, 10, 15],
                index=1,
            )

        st.markdown("**Include sections:**")
        col_inc1, col_inc2, col_inc3, col_inc4 = st.columns(4)
        with col_inc1:
            include_mcq = st.checkbox("Multiple-choice questions", value=True)
        with col_inc2:
            include_scenarios = st.checkbox("Scenario questions", value=True)
        with col_inc3:
            include_reflection = st.checkbox("Reflection questions", value=True)
        with col_inc4:
            include_answers = st.checkbox("Answer key", value=True)

        st.markdown("---")

        if st.button("Generate Knowledge Check", type="primary"):
            with st.spinner("Generating knowledge check..."):
                check = kc.generate_knowledge_check(
                    scenario,
                    assessment=assessment,
                    workshop_plan=workshop_plan,
                    activities=activities,
                    facilitator_guide=facilitator_guide_data,
                    handout=staff_handout,
                    question_count=question_count_choice,
                )
                check_md = kc.format_knowledge_check_as_markdown(
                    check, include_answer_key=include_answers
                )
                check_filename = kc.create_knowledge_check_filename(
                    scenario.get("organisation_name", "organisation")
                )
                st.session_state["knowledge_check"] = check
                st.session_state["knowledge_check_markdown"] = check_md
                st.session_state["knowledge_check_filename"] = check_filename
                pdf_bytes, pdf_filename = _generate_report_pdf(
                    check_md, "Knowledge Check", scenario
                )
                st.session_state["knowledge_check_pdf_bytes"] = pdf_bytes
                st.session_state["knowledge_check_pdf_filename"] = pdf_filename
            st.success("Knowledge check generated.")
            st.rerun()

        if "knowledge_check" in st.session_state:
            check = st.session_state["knowledge_check"]
            check_summary = kc.summarise_knowledge_check(check)

            st.markdown("---")
            st.markdown("#### Summary")

            c1, c2, c3, c4, c5 = st.columns(5)
            c1.metric("Organisation", check_summary["organisation_name"])
            c2.metric("MCQs", check_summary["mcq_count"])
            c3.metric("Scenario questions", check_summary["scenario_question_count"])
            c4.metric("Reflection questions", check_summary["reflection_question_count"])
            c5.metric("Answer key", "Yes" if check_summary["answer_key_included"] else "No")

            st.markdown("---")
            st.markdown(f"#### {check['knowledge_check_title']}")
            st.markdown(f"**Audience:** {', '.join(check.get('audience', []))}")
            st.info(check.get("purpose", ""))

            st.markdown("---")
            st.markdown("**Instructions**")
            st.markdown(check.get("instructions", ""))

            if include_mcq and check.get("multiple_choice_questions"):
                st.markdown("---")
                st.markdown("#### Multiple-Choice Questions")
                for q in check["multiple_choice_questions"]:
                    with st.expander(
                        f"{q['question_id'].upper()} — {q['question'][:80]}…"
                        if len(q["question"]) > 80
                        else f"{q['question_id'].upper()} — {q['question']}"
                    ):
                        st.markdown(f"**Topic:** {q['topic']}")
                        st.markdown(f"**{q['question']}**")
                        for letter, text in q["options"].items():
                            st.markdown(f"{letter}. {text}")

            if include_scenarios and check.get("scenario_questions"):
                st.markdown("---")
                st.markdown("#### Scenario Questions")
                for q in check["scenario_questions"]:
                    with st.expander(
                        f"{q['question_id'].upper()} — {q['topic'].title()}"
                    ):
                        st.markdown(f"**Scenario:** *{q['scenario']}*")
                        st.markdown(f"**Question:** {q['question']}")

            if include_reflection and check.get("reflection_questions"):
                st.markdown("---")
                st.markdown("#### Reflection Questions")
                for q in check["reflection_questions"]:
                    st.markdown(f"**{q['question_id'].upper()}.** {q['question']}")
                    st.markdown("")

            if include_answers and check.get("answer_key"):
                st.markdown("---")
                with st.expander("Answer Key (facilitator / trainer use only)"):
                    answer_key = check["answer_key"]
                    st.caption(answer_key.get("marking_note", ""))
                    st.markdown("**Multiple-Choice Answers**")
                    for answer in answer_key.get("multiple_choice_answers", []):
                        st.markdown(
                            f"- **{answer['question_id'].upper()}:** "
                            f"Correct answer: **{answer['correct_answer']}** — "
                            f"{answer['explanation']}"
                        )
                    st.markdown("**Scenario Answer Guidance**")
                    for guidance in answer_key.get("scenario_answer_guidance", []):
                        st.markdown(f"**{guidance['question_id'].upper()} — {guidance['topic'].title()}**")
                        st.markdown(f"*Model answer:* {guidance['model_answer']}")
                        st.markdown("Key points:")
                        for point in guidance.get("expected_answer_points", []):
                            st.markdown(f"- {point}")
                    st.markdown("**Reflection Guidance**")
                    for guidance in answer_key.get("reflection_guidance", []):
                        st.markdown(f"**{guidance['question_id'].upper()} — {guidance['topic'].title()}**")
                        for point in guidance.get("guidance_points", []):
                            st.markdown(f"- {point}")

            st.markdown("---")
            st.markdown("#### Pass and Review Guidance")
            st.markdown(check.get("pass_guidance", ""))
            st.markdown(check.get("review_guidance", ""))

            st.markdown("---")
            st.warning(check.get("responsible_use_warning", ""), icon="⚠️")

            st.markdown("---")
            _render_report_downloads(
                md_text=st.session_state.get("knowledge_check_markdown", ""),
                md_filename=st.session_state.get("knowledge_check_filename", "knowledge-check.md"),
                md_label="Download Knowledge Check (Markdown)",
                pdf_bytes_key="knowledge_check_pdf_bytes",
                pdf_filename_key="knowledge_check_pdf_filename",
                pdf_label="Download PDF Knowledge Check",
            )

elif page == "Training Pack Export":
    ui.render_page_header(
        "Training Pack Export",
        "Combine all generated outputs into one downloadable Markdown training pack.",
    )
    ui.render_responsible_use_warning()
    st.markdown("---")

    readiness = tp.check_training_pack_readiness(dict(st.session_state))

    if not readiness["is_ready"]:
        st.warning("No scenario loaded. Complete these steps first:")
        st.markdown(
            "1. Go to **Organisation Scenario** in the sidebar.\n"
            "2. Click **Load BrightPath Demo Scenario** or fill in the form.\n"
            "3. Click **Save Scenario**.\n"
            "4. Return here to export the Training Pack."
        )
    else:
        # Readiness overview
        st.markdown("#### Training Pack Readiness")

        col_avail, col_miss = st.columns(2)
        with col_avail:
            if readiness["available_sections"]:
                st.markdown("**Available sections:**")
                for s in readiness["available_sections"]:
                    st.markdown(f"- ✓ {s}")
        with col_miss:
            if readiness["missing_sections"]:
                st.markdown("**Recommended but not yet generated:**")
                for s in readiness["missing_sections"]:
                    st.markdown(f"- ○ {s}")
                st.info(
                    "Run the earlier pages to include these sections. "
                    "The pack can still be exported with available sections."
                )

        st.markdown("---")
        st.markdown("#### Select Sections to Include")

        section_labels = {
            "scenario": "Organisation Scenario Summary",
            "training_needs_assessment": "Training Needs Assessment",
            "workshop_plan": "Workshop Plan",
            "training_activities": "Training Activities",
            "facilitator_guide": "Facilitator Guide",
            "staff_handout": "Staff Handout",
            "knowledge_check": "Knowledge Check",
            "answer_key": "Answer Key",
            "facilitator_review_checklist": "Facilitator Review Checklist",
            "responsible_use_boundaries": "Responsible-Use Boundaries",
            "prototype_limitations": "Prototype Limitations",
            "recommended_next_steps": "Recommended Next Steps",
        }

        avail_keys = {
            "scenario": bool(st.session_state.get("training_scenario")),
            "training_needs_assessment": bool(st.session_state.get("training_needs_assessment")),
            "workshop_plan": bool(st.session_state.get("workshop_plan")),
            "training_activities": bool(st.session_state.get("training_activities")),
            "facilitator_guide": bool(st.session_state.get("facilitator_guide")),
            "staff_handout": bool(st.session_state.get("staff_handout")),
            "knowledge_check": bool(st.session_state.get("knowledge_check")),
            "answer_key": bool(st.session_state.get("knowledge_check")),
            "facilitator_review_checklist": True,
            "responsible_use_boundaries": True,
            "prototype_limitations": True,
            "recommended_next_steps": True,
        }

        col1, col2, col3 = st.columns(3)
        include_sections = {}
        section_keys = list(section_labels.keys())
        for i, key in enumerate(section_keys):
            col = [col1, col2, col3][i % 3]
            with col:
                default = avail_keys.get(key, True)
                include_sections[key] = st.checkbox(
                    section_labels[key],
                    value=default,
                    key=f"include_{key}",
                )

        st.markdown("---")

        if st.button("Generate Training Pack", type="primary"):
            with st.spinner("Assembling training pack..."):
                pack_data = tp.build_training_pack_data_from_session_state(
                    dict(st.session_state)
                )
                pack_md = tp.generate_markdown_training_pack(pack_data, include_sections)
                pack_filename = tp.create_training_pack_filename(
                    st.session_state.get("training_scenario", {}).get(
                        "organisation_name", "organisation"
                    )
                )
                st.session_state["training_pack_data"] = pack_data
                st.session_state["training_pack_markdown"] = pack_md
                st.session_state["training_pack_filename"] = pack_filename
                st.session_state["training_pack_readiness"] = readiness
                _org = st.session_state.get("training_scenario", {}).get(
                    "organisation_name", "training-pack"
                )
                _analytics = {}
                try:
                    _analytics = ra.build_training_pack_analytics(pack_data)
                    st.session_state["training_pack_analytics"] = _analytics
                except Exception:
                    st.session_state["training_pack_analytics"] = {}

                try:
                    st.session_state["training_pack_pdf_bytes"] = eu.export_training_pack_to_pdf(
                        pack_data, pack_md, analytics=_analytics
                    )
                    st.session_state["training_pack_pdf_filename"] = eu.create_safe_filename(
                        f"training-pack-{_org}", "pdf"
                    )
                except Exception:
                    st.session_state["training_pack_pdf_bytes"] = None

                try:
                    st.session_state["training_pack_pptx_bytes"] = ppt.export_training_pack_to_pptx_bytes(
                        pack_data, analytics=_analytics
                    )
                    st.session_state["training_pack_pptx_filename"] = ppt.create_safe_pptx_filename(
                        f"training-pack-{_org}"
                    )
                except Exception:
                    st.session_state["training_pack_pptx_bytes"] = None
                    st.session_state["training_pack_pptx_filename"] = None
            st.success("Training pack assembled.")
            st.rerun()

        if "training_pack_data" in st.session_state:
            pack_data = st.session_state["training_pack_data"]
            pack_summary = tp.summarise_training_pack(pack_data)

            st.markdown("---")
            st.markdown("#### Summary")

            c1, c2, c3, c4, c5 = st.columns(5)
            c1.metric("Organisation", pack_summary["organisation_name"])
            c2.metric(
                "Sections available",
                f"{pack_summary['sections_available']} / {pack_summary['sections_total']}",
            )
            c3.metric("Activities", pack_summary["activity_count"])
            c4.metric("MCQs", pack_summary["mcq_count"])
            c5.metric("Answer key", "Yes" if pack_summary["answer_key_included"] else "No")

            st.markdown(f"**Generated:** {pack_summary['generated_date']}")

            st.markdown("---")
            st.markdown("#### Facilitator Review Checklist")
            st.markdown("Before delivering this training pack, confirm:")
            for item in tp.generate_facilitator_review_checklist():
                st.markdown(f"- ☐ {item}")

            st.markdown("---")
            st.markdown("#### Recommended Next Steps")
            for step in tp.generate_training_pack_next_steps(pack_data):
                st.markdown(f"- {step}")

            # ── Analytics ─────────────────────────────────────────────────────
            st.markdown("---")
            st.markdown("#### Training Pack Analytics")

            analytics = ra.build_training_pack_analytics(pack_data)
            st.session_state["training_pack_analytics"] = analytics

            report_quality = analytics.get("report_quality", {})
            completeness = report_quality.get("completeness_pct", 0)
            st.markdown(
                f"**Pack completeness:** {completeness}% "
                f"({report_quality.get('sections_available', 0)} of "
                f"{report_quality.get('sections_total', 7)} sections generated)"
            )

            # Chart row
            try:
                _charts = eu.generate_chart_images_for_training_pack(pack_data, analytics)
                _chart_cols = [k for k in ["section_completion", "topic_coverage", "activity_mix"] if k in _charts]
                if _chart_cols:
                    _cols = st.columns(min(len(_chart_cols), 3))
                    _labels = {
                        "section_completion": "Section Completion",
                        "topic_coverage": "Priority Topics",
                        "activity_mix": "Activity Mix",
                    }
                    for _col, _chart_key in zip(_cols, _chart_cols):
                        with _col:
                            st.image(_charts[_chart_key], caption=_labels.get(_chart_key, ""), use_container_width=True)

                _time_cols = [k for k in ["time_allocation", "kc_topic_coverage"] if k in _charts]
                if _time_cols:
                    _cols2 = st.columns(len(_time_cols))
                    _labels2 = {"time_allocation": "Workshop Time Allocation", "kc_topic_coverage": "Knowledge Check Topics"}
                    for _col, _ck in zip(_cols2, _time_cols):
                        with _col:
                            st.image(_charts[_ck], caption=_labels2.get(_ck, ""), use_container_width=True)
            except Exception:
                st.caption("Charts not available for this session.")

            # ── Markdown preview ───────────────────────────────────────────────
            st.markdown("---")
            st.markdown("#### Markdown Preview")
            pack_md = st.session_state.get("training_pack_markdown", "")
            with st.expander("Preview training pack Markdown (first 4,000 characters)"):
                st.code(pack_md[:4000] + ("…" if len(pack_md) > 4000 else ""), language="markdown")

            # ── Export options ─────────────────────────────────────────────────
            st.markdown("---")
            ui.render_export_options_panel()

            _org_name = st.session_state.get("training_scenario", {}).get("organisation_name", "training-pack")
            pack_filename = st.session_state.get("training_pack_filename", "training-pack.md")

            col_md, col_pdf, col_pptx = st.columns(3)

            with col_md:
                st.markdown("**Markdown**")
                if pack_md:
                    st.download_button(
                        label="Download Markdown Training Pack",
                        data=pack_md,
                        file_name=pack_filename,
                        mime="text/markdown",
                        use_container_width=True,
                    )

            with col_pdf:
                st.markdown("**PDF**")
                if st.button("Generate PDF", key="gen_pdf", use_container_width=True):
                    with st.spinner("Generating PDF..."):
                        try:
                            _pdf_bytes = eu.export_training_pack_to_pdf(
                                pack_data, pack_md, analytics=analytics
                            )
                            st.session_state["training_pack_pdf_bytes"] = _pdf_bytes
                            st.success("PDF ready.")
                        except Exception as _e:
                            st.error(f"PDF generation failed: {_e}")
                if st.session_state.get("training_pack_pdf_bytes"):
                    _pdf_filename = st.session_state.get(
                        "training_pack_pdf_filename",
                        eu.create_safe_filename(f"training-pack-{_org_name}", "pdf"),
                    )
                    st.download_button(
                        label="Download PDF Training Pack",
                        data=st.session_state["training_pack_pdf_bytes"],
                        file_name=_pdf_filename,
                        mime="application/pdf",
                        use_container_width=True,
                        key="dl_pdf",
                    )

            with col_pptx:
                st.markdown("**PowerPoint**")
                if not st.session_state.get("training_pack_pptx_bytes"):
                    if st.button("Generate PowerPoint", key="gen_pptx", use_container_width=True):
                        with st.spinner("Generating PowerPoint..."):
                            try:
                                _pptx_bytes = ppt.export_training_pack_to_pptx_bytes(
                                    pack_data, analytics=analytics
                                )
                                st.session_state["training_pack_pptx_bytes"] = _pptx_bytes
                                st.session_state["training_pack_pptx_filename"] = (
                                    ppt.create_safe_pptx_filename(f"training-pack-{_org_name}")
                                )
                                st.success("PowerPoint ready.")
                            except Exception as _e:
                                st.error(f"PowerPoint generation failed: {_e}")
                if st.session_state.get("training_pack_pptx_bytes"):
                    _pptx_filename = st.session_state.get(
                        "training_pack_pptx_filename",
                        ppt.create_safe_pptx_filename(f"training-pack-{_org_name}"),
                    )
                    st.download_button(
                        label="Download PowerPoint Training Deck",
                        data=st.session_state["training_pack_pptx_bytes"],
                        file_name=_pptx_filename,
                        mime="application/vnd.openxmlformats-officedocument.presentationml.presentation",
                        use_container_width=True,
                        key="dl_pptx",
                    )

            st.markdown("---")
            ui.render_report_quality_notice()
