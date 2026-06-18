import streamlit as st


def apply_global_styles():
    st.markdown("""
    <style>
    [data-testid="stSidebar"] {
        background-color: #1a2744;
    }
    [data-testid="stSidebar"] * {
        color: #ffffff !important;
    }
    .info-card {
        background: #f0f4ff;
        border-left: 4px solid #1a2744;
        border-radius: 4px;
        padding: 12px 16px;
        margin: 8px 0;
    }
    </style>
    """, unsafe_allow_html=True)


def render_page_header(title: str, subtitle: str = ""):
    st.title(title)
    if subtitle:
        st.markdown(f"*{subtitle}*")
    st.divider()


def render_responsible_use_warning():
    st.warning(
        "**Responsible Use:** This prototype uses synthetic/demo data only. "
        "Do not use with real client records, learner data, safeguarding case details, "
        "staff HR data, personal data, confidential data, or regulated information. "
        "Outputs are not legal, safeguarding, HR, compliance, or professional advice. "
        "Human review is required before any real-world use."
    )


def render_prototype_notice():
    st.info(
        "**Prototype:** Production-style AI governance review prototype, not a production "
        "compliance, legal, safeguarding, HR, data-protection, or professional advisory system."
    )


def render_info_card(title: str, body: str):
    st.markdown(
        f'<div class="info-card"><strong>{title}</strong><br>{body}</div>',
        unsafe_allow_html=True,
    )


def render_status_box(message: str, status_type: str = "info"):
    if status_type == "warning":
        st.warning(message)
    elif status_type == "success":
        st.success(message)
    elif status_type == "error":
        st.error(message)
    else:
        st.info(message)


def render_metric_row(metrics: list):
    cols = st.columns(len(metrics))
    for col, metric in zip(cols, metrics):
        with col:
            col.metric(
                label=metric.get("label", ""),
                value=metric.get("value", ""),
                delta=metric.get("delta", None),
            )


def render_completion_badge(label: str, is_complete: bool):
    icon = "✅" if is_complete else "⬜"
    st.sidebar.markdown(f"{icon} {label}")


def render_workflow_steps(steps: list, current_step: int = 0):
    for i, step in enumerate(steps):
        if i < current_step:
            st.markdown(f"✅ ~~{step}~~")
        elif i == current_step:
            st.markdown(f"**→ {step}**")
        else:
            st.markdown(f"⬜ {step}")
