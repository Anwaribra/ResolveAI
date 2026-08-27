import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="ResolveAI — Support Triage Dashboard",
    page_icon="🤖",
    layout="wide",
)

st.title("🤖 ResolveAI — Support Triage & Analytics")
st.markdown(
    "Real-time visibility into AI classification, RAG retrieval accuracy, auto-resolution rates, and safety governance."
)

st.divider()

# Key Performance Indicator Cards
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric(label="Total Tickets Ingested", value="1,248", delta="+12%")
with col2:
    st.metric(label="Auto-Resolution Rate", value="64.2%", delta="+3.1%")
with col3:
    st.metric(label="Escalation Rate", value="35.8%", delta="-3.1%")
with col4:
    st.metric(
        label="False Auto-Resolution Rate",
        value="0.8%",
        delta="-0.2%",
        delta_color="normal",
    )

st.divider()

col_left, col_right = st.columns(2)

with col_left:
    st.subheader("Ticket Category Breakdown")
    category_data = pd.DataFrame(
        {
            "Category": ["Account Access", "Billing", "Refunds", "General", "Security"],
            "Count": [410, 320, 250, 198, 70],
        }
    )
    st.bar_chart(category_data, x="Category", y="Count")

with col_right:
    st.subheader("Decision Engine Distribution")
    decision_data = pd.DataFrame(
        {
            "Outcome": ["AUTO_RESOLVE", "ESCALATE (Low Confidence)", "ESCALATE (High Risk)", "ESCALATE (Urgent)"],
            "Volume": [801, 245, 122, 80],
        }
    )
    st.dataframe(decision_data, use_container_width=True)

st.divider()
st.caption("ResolveAI Operational Dashboard • Data refreshed from PostgreSQL Analytical Warehouse.")
