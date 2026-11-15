import sys
import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
if str(BASE_DIR) not in sys.path:
    sys.path.append(str(BASE_DIR))

import streamlit as st
from utils.data_loader import load_data
from utils.report_generator import generate_pdf_report
from utils.project_doc_generator import generate_combined_project_documentation
from utils.dashboard_metrics import (
    render_page_header,
    render_kpi_card,
    compute_executive_summary,
    render_footer,
)

st.set_page_config(
    page_title="AI Intelligence Report Generator | Threat Intelligence",
    page_icon="📄",
    layout="wide",
)

render_page_header(
    title="📄 Strategic Intelligence Dossier & Report Generator",
    subtitle="Interactive Executive Briefing Preview & Automated ReportLab PDF Dossier Compilation",
    badge_text="DOSSIER SYNTHESIS",
)

try:
    df = load_data()
except Exception as e:
    st.error(f"❌ Failed to initialize core dataset pipeline for parameters: {e}")
    st.stop()

st.subheader("🛠️ Scope Filter Configurations")
col1, col2 = st.columns(2)

with col1:
    filter_type = st.radio(
        "Select Geographical Aggregation Layer:",
        options=["Global Overview", "By Specific Country", "By Specific Region"],
        horizontal=True,
        help="Determines the physical filtering bounds applied to the generated metrics.",
    )

selected_country = None
selected_region = None
scoped_df = df.copy()

with col2:
    if filter_type == "By Specific Country":
        available_countries = sorted(df["country_txt"].dropna().unique())
        selected_country = st.selectbox("🎯 Target Country Selection Profile", options=available_countries)
        scoped_df = df[df["country_txt"] == selected_country]
    elif filter_type == "By Specific Region":
        available_regions = sorted(df["region_txt"].dropna().unique())
        selected_region = st.selectbox("🌐 Target Region Selection Profile", options=available_regions)
        scoped_df = df[df["region_txt"] == selected_region]
    else:
        st.info(f"ℹ️ System will compile full global dataset limits ({len(df):,} validated records).")

scope_name = selected_country or selected_region or "Global Overview"
summary = compute_executive_summary(scoped_df)

# Live Executive Dossier Preview on Screen
st.markdown("---")
st.subheader(f"📋 Live Executive Briefing Preview — {scope_name}")

k1, k2, k3, k4 = st.columns(4)
with k1:
    render_kpi_card("Scoped Incidents", f"{summary['total_incidents']:,}", f"Peak Year: {summary['peak_year']}", "#3b82f6")
with k2:
    render_kpi_card("Confirmed Fatalities", f"{summary['total_fatalities']:,}", f"Injuries: {summary['total_injuries']:,}", "#ef4444")
with k3:
    render_kpi_card("Dominant Attack Tactic", summary["top_attack"], f"Weapon: {summary['top_weapon']}", "#f59e0b")
with k4:
    render_kpi_card("Primary Target Sector", summary["top_target"], f"Success Rate: {summary['success_rate']:.1f}%", "#10b981")

st.markdown(
    f"""
    <div class='kpi-card' style='padding:22px;'>
        <h4 style='color:#60a5fa; margin-top:0;'>📑 Automated Intelligence Synthesis — {scope_name}</h4>
        <p style='color:#cbd5e1; line-height:1.65; margin-bottom:8px;'>
            Across the evaluated historical window, <strong>{scope_name}</strong> logged
            <strong>{summary['total_incidents']:,}</strong> verified security incidents resulting in
            <strong>{summary['total_casualties']:,}</strong> combined casualties
            (<strong>{summary['total_fatalities']:,}</strong> fatalities and <strong>{summary['total_injuries']:,}</strong> injuries),
            with an overall operational execution rate of <strong>{summary['success_rate']:.1f}%</strong>.
        </p>
        <p style='color:#cbd5e1; line-height:1.65; margin-bottom:0;'>
            Tactical pattern distribution indicates that <strong>{summary['top_attack']}</strong> serves as the primary
            operational vector, predominantly leveraging <strong>{summary['top_weapon']}</strong> against
            <strong>{summary['top_target']}</strong> infrastructure.
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)

# PDF Compilation & Export Controls
st.subheader("🚀 Document Synthesis & Export Engine")
OUTPUT_PATH = str(BASE_DIR / "reports" / "executive_intelligence_briefing.pdf")

btn_col1, btn_col2, btn_col3 = st.columns(3)
with btn_col1:
    if st.button("📊 Compile Executive PDF Dossier", type="primary", width='stretch'):
        with st.spinner("Parsing data bounds, designing tables, and building ReportLab PDF layout..."):
            try:
                generate_pdf_report(
                    df=df,
                    selected_country=selected_country,
                    selected_region=selected_region,
                    output_filename=OUTPUT_PATH,
                )

                if os.path.exists(OUTPUT_PATH):
                    st.success("✅ Executive Briefing compiled and saved successfully.")
                    with open(OUTPUT_PATH, "rb") as f:
                        pdf_bytes = f.read()

                    st.download_button(
                        label="📥 Download Executive PDF Report File",
                        data=pdf_bytes,
                        file_name=f"GTD_Intelligence_Briefing_{selected_country or selected_region or 'Global'}.pdf",
                        mime="application/pdf",
                        width='stretch',
                    )
                else:
                    st.error("❌ Synthesis completed, but output PDF file was not located.")
            except Exception as e:
                st.error(f"❌ Document compilation failed unexpectedly: {e}")

with btn_col2:
    doc_pdf_path = generate_combined_project_documentation()
    if os.path.exists(doc_pdf_path):
        with open(doc_pdf_path, "rb") as f_doc:
            doc_bytes = f_doc.read()
        st.download_button(
            label="📘 Download Combined Project Documentation (PDF)",
            data=doc_bytes,
            file_name="Global_Threat_Intelligence_Project_Documentation.pdf",
            mime="application/pdf",
            width='stretch',
        )

with btn_col3:
    csv_bytes = scoped_df.to_csv(index=False).encode("utf-8")
    st.download_button(
        label="📊 Export Scoped Dataset Slice (CSV)",
        data=csv_bytes,
        file_name=f"GTD_Scoped_Data_{selected_country or selected_region or 'Global'}.csv",
        mime="text/csv",
        width='stretch',
    )

render_footer(
    "**⚠️ METHODOLOGICAL SAFEGUARD NOTICE:** The generated PDF documentation consists entirely of rule-based retrospective data summaries "
    "collated from historical variance parameters inside the Global Terrorism Database (GTD). "
    "They serve exclusively as explainable decision-support files for academic, historical retrospective review."
)
