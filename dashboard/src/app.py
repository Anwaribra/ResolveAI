import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

st.set_page_config(
    page_title="ResolveAI — Support Triage & Auto-Resolution Dashboard",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS styling for premium look
st.markdown("""
<style>
    .main-header {
        font-size: 2.2rem;
        font-weight: 700;
        background: linear-gradient(90deg, #3B82F6 0%, #8B5CF6 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.5rem;
    }
    .metric-card {
        background-color: #1E293B;
        border-radius: 12px;
        padding: 1.2rem;
        border: 1px solid #334155;
    }
    .badge-auto {
        background-color: #10B981;
        color: white;
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 0.85rem;
        font-weight: 600;
    }
    .badge-escalate {
        background-color: #EF4444;
        color: white;
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 0.85rem;
        font-weight: 600;
    }
</style>
""", unsafe_allow_html=True)

# Sidebar filters
st.sidebar.title("ResolveAI Control Panel")
st.sidebar.markdown("---")

environment_filter = st.sidebar.selectbox("Environment", ["Production", "Staging", "Development"])
date_range = st.sidebar.date_input("Date Range", [datetime.now() - timedelta(days=7), datetime.now()])
provider_setting = st.sidebar.selectbox("LLM Provider Active", ["Gemini 2.5 Flash (Primary)", "OpenRouter Claude 3.5 (Fallback)"])

st.sidebar.markdown("---")
st.sidebar.subheader("System Health")
st.sidebar.success("PostgreSQL + pgvector: Connected")
st.sidebar.success("Airflow Scheduler: Healthy")
st.sidebar.success("Decision Engine: Operational")

# Header
st.markdown('<p class="main-header">ResolveAI — Support Triage & Auto-Resolution Agent</p>', unsafe_allow_html=True)
st.markdown("Joint Data Engineering & AI Platform • Operational Monitoring, RAG Retrieval Inspection & Risk Governance")

st.divider()

# Navigation Tabs
tab_overview, tab_live_triage, tab_rag_inspector, tab_eval = st.tabs([
    "Overview & Analytics",
    "Live Ticket Triage Simulator",
    "RAG & Knowledge Inspector",
    "Safety & Model Evaluation"
])

# ---------------- TAB 1: OVERVIEW ----------------
with tab_overview:
    # Key Metrics KPI Row
    kpi1, kpi2, kpi3, kpi4, kpi5 = st.columns(5)
    
    with kpi1:
        st.metric(label="Total Tickets Ingested", value="1,420", delta="+14.2% vs last week")
    with kpi2:
        st.metric(label="Auto-Resolution Rate", value="68.4%", delta="+4.2%")
    with kpi3:
        st.metric(label="Human Escalation Rate", value="31.6%", delta="-4.2%")
    with kpi4:
        st.metric(label="False Auto-Resolution Rate", value="0.75%", delta="-0.15%", delta_color="normal")
    with kpi5:
        st.metric(label="Human Hours Saved", value="142 hrs", delta="+18 hrs")

    st.divider()

    col_chart1, col_chart2 = st.columns(2)
    
    with col_chart1:
        st.subheader("Daily Ticket Volume & Resolution Channel")
        dates = [datetime.now() - timedelta(days=i) for i in range(7)][::-1]
        df_trends = pd.DataFrame({
            "Date": [d.strftime("%b %d") for d in dates],
            "AUTO_RESOLVED": [140, 155, 162, 178, 190, 185, 195],
            "ESCALATED": [70, 68, 65, 62, 58, 60, 55],
        })
        st.line_chart(df_trends.set_index("Date"))

    with col_chart2:
        st.subheader("Decision Engine Distribution by Category")
        category_df = pd.DataFrame({
            "Category": ["Account Access", "Billing Inquiry", "Refund Request", "General Info", "Security Breach"],
            "Auto Resolved": [420, 310, 210, 180, 0],
            "Escalated": [40, 90, 70, 30, 85]
        })
        st.bar_chart(category_df.set_index("Category"))

    st.divider()

    st.subheader("Recent Ticket Processing Log")
    recent_tickets = pd.DataFrame([
        {"Ticket ID": "TKT-8841", "Subject": "Account locked after failed password attempts", "Category": "Account Access", "Priority": "medium", "Confidence": 0.96, "Retrieval Quality": 0.92, "Decision": "AUTO_RESOLVE", "Time": "2 mins ago"},
        {"Ticket ID": "TKT-8840", "Subject": "Potential security vulnerability report", "Category": "Security Breach", "Priority": "urgent", "Confidence": 0.98, "Retrieval Quality": 0.70, "Decision": "ESCALATE", "Time": "12 mins ago"},
        {"Ticket ID": "TKT-8839", "Subject": "Need refund for last month charge", "Category": "Refund Request", "Priority": "medium", "Confidence": 0.89, "Retrieval Quality": 0.85, "Decision": "AUTO_RESOLVE", "Time": "25 mins ago"},
        {"Ticket ID": "TKT-8838", "Subject": "API latency issues in prod region us-east", "Category": "Technical Issue", "Priority": "high", "Confidence": 0.78, "Retrieval Quality": 0.65, "Decision": "ESCALATE", "Time": "41 mins ago"},
    ])
    st.dataframe(recent_tickets, use_container_width=True)

# ---------------- TAB 2: LIVE TICKET TRIAGE SIMULATOR ----------------
with tab_live_triage:
    st.subheader("Live Ticket Processing & Decision Engine Simulator")
    st.markdown("Test ticket classification, vector context retrieval, grounded answer generation, and decision engine risk governance in real time.")
    
    col_input, col_output = st.columns([1, 1])
    
    with col_input:
        sim_email = st.text_input("Customer Email", "john.doe@enterprise.com")
        sim_tier = st.selectbox("Customer Tier", ["enterprise", "premium", "standard"])
        sim_subject = st.text_input("Ticket Subject", "Locked out of my account after multiple attempts")
        sim_body = st.text_area(
            "Ticket Message Body",
            "Hi support team,\n\nI tried logging into my account 5 times with the wrong password and now it says 'Account locked'. Can you please help me get back in?",
            height=140
        )
        run_btn = st.button("Process Ticket with ResolveAI", type="primary", use_container_width=True)

    with col_output:
        if run_btn:
            st.success("Ticket Processed Successfully!")
            
            # Simulated AI outputs
            st.markdown("### AI Classification & Triage")
            c1, c2, c3 = st.columns(3)
            c1.metric("Category", "account_access")
            c2.metric("Intent", "unlock_account")
            c3.metric("Priority", "medium")
            
            st.markdown("### RAG Knowledge Search")
            st.info("Top Match: account_locked.md (Similarity: 0.94)")
            
            st.markdown("### Grounded Response Generation")
            st.text_area(
                "Generated Customer Response",
                "Hi John,\n\nYour account was automatically locked after 5 failed password attempts to secure your data. You can unlock your account immediately by requesting a magic link at https://app.example.com/unlock using your registered email address.\n\nBest regards,\nResolveAI Support",
                height=130
            )
            
            st.markdown("### Decision Engine Evaluation")
            st.markdown(r"""
            - **Confidence Score**: `0.94` (Threshold: $\ge 0.85$) - MET
            - **Retrieval Quality**: `0.94` (Threshold: $\ge 0.80$) - MET
            - **Risk Profile**: `LOW` (Non-security, non-urgent) - MET
            """)
            st.markdown('<span class="badge-auto">FINAL DECISION: AUTO_RESOLVE</span>', unsafe_allow_html=True)
        else:
            st.info("Fill out ticket details on the left and click **Process Ticket** to test the pipeline.")

# ---------------- TAB 3: RAG INSPECTOR ----------------
with tab_rag_inspector:
    st.subheader("Knowledge Base Vector Search & Document Chunk Inspector")
    st.markdown("Inspect local markdown knowledge base documents and pgvector embeddings stored in PostgreSQL.")
    
    selected_doc = st.selectbox(
        "Select Knowledge Document",
        ["account_locked.md", "password_reset.md", "payment_failed.md", "refund_policy.md", "subscription.md", "shipping.md"]
    )
    
    doc_col1, doc_col2 = st.columns([1, 1])
    
    with doc_col1:
        st.markdown(f"### Document Preview: `{selected_doc}`")
        if selected_doc == "account_locked.md":
            st.code("""# Account Locked Troubleshooting Policy
1. Accounts lock automatically after 5 consecutive failed login attempts.
2. Users can unlock immediately at https://app.example.com/unlock via email link.
3. Lock duration is 30 minutes by default.""", language="markdown")
        elif selected_doc == "refund_policy.md":
            st.code("""# Official Refund Policy
1. Full 30-day money-back guarantee for all subscription products.
2. Refund requests processed back to original payment method within 5-7 business days.""", language="markdown")
        else:
            st.code(f"# {selected_doc}\nSample policy content for {selected_doc}.", language="markdown")

    with doc_col2:
        st.markdown("### Vector Embeddings (`pgvector`) Metadata")
        st.json({
            "document_id": "doc-89a3f2-8811",
            "file_name": selected_doc,
            "vector_dimension": 768,
            "index_type": "HNSW (vector_cosine_ops)",
            "chunk_count": 3,
            "last_embedded_at": "2026-08-27 18:30:00 UTC"
        })

# ---------------- TAB 4: EVALUATION & SAFETY ----------------
with tab_eval:
    st.subheader("Offline Evaluation Harness & Safety Thresholds")
    
    e1, e2, e3 = st.columns(3)
    e1.metric("Classification Accuracy", "96.4%", "Target: >95%")
    e2.metric("Retrieval Precision @ k=3", "92.1%", "Target: >90%")
    e3.metric("Answer Groundedness Score", "98.7%", "Target: >98%")
    
    st.divider()
    st.subheader("Safety Metric: False Auto-Resolution Tracking")
    st.markdown("""
    The **False Auto-Resolution Rate** measures the percentage of tickets automatically resolved by AI that ultimately required reopening or human correction.
    Target Threshold is strictly **< 2.0%**.
    """)
    
    false_res_df = pd.DataFrame({
        "Week": ["Week 1", "Week 2", "Week 3", "Week 4"],
        "False Auto-Resolution Rate (%)": [1.4, 1.1, 0.9, 0.75]
    })
    st.line_chart(false_res_df.set_index("Week"))
