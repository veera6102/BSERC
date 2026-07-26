import streamlit as st
import os
from utils.data_loader import load_data
from utils.report_generator import generate_pdf_report

# 1. Page Configuration
st.set_page_config(
    page_title="AI Intelligence Report Generator | Threat Intelligence",
    page_icon="📄",
    layout="wide"
)

st.markdown("<h1 class='glow-text'>📄 Strategic AI Intelligence Report Generator</h1>", unsafe_allow_html=True)
st.markdown("<p style='color:#94a3b8;font-size:1.1rem;'>Compile and Export Tailored Multi-Sector Retrospective Data Summaries into Production-Grade PDFs.</p>", unsafe_allow_html=True)
st.markdown("<hr style='border-color:rgba(59, 130, 246, 0.2);'>", unsafe_allow_html=True)

# 2. Safely Load Master Data Context
try:
    df = load_data()
except Exception as e:
    st.error(f"❌ Failed to initialize core dataset pipeline for parameters: {e}")
    st.stop()

# 3. Parameter Selection Panel
st.subheader("🛠️ Scope Filter Configurations")
col1, col2 = st.columns(2)

with col1:
    filter_type = st.radio(
        "Select Geographical Aggregation Layer:",
        options=["Global Overview", "By Specific Country", "By Specific Region"],
        horizontal=True,
        help="Determines the physical filtering bounds applied to the generated metrics."
    )

# Compute values based on radio selections
selected_country = None
selected_region = None

with col2:
    if filter_type == "By Specific Country":
        available_countries = sorted(df["country_txt"].dropna().unique())
        selected_country = st.selectbox("🎯 Target Country Selection Profile", options=available_countries)
    elif filter_type == "By Specific Region":
        available_regions = sorted(df["region_txt"].dropna().unique())
        selected_region = st.selectbox("🌐 Target Region Selection Profile", options=available_regions)
    else:
        st.info("ℹ️ System will compile full global dataset limits (209,706 raw records).")

st.markdown("<br>", unsafe_allow_html=True)

# 4. Report Compiling and Execution
st.subheader("🚀 Document Synthesis Engine")
st.markdown("Clicking the trigger below passes filters to the backend ReportLab utility to build standard canvas tables and flowables:")

OUTPUT_PATH = "reports/executive_intelligence_briefing.pdf"

if st.button("📊 Compile Executive PDF Dossier", type="primary", use_container_width=True):
    with st.spinner("Parsing data bounds, designing tables, and building layouts..."):
        try:
            # Execute backend PDF compiling engine
            generate_pdf_report(
                df=df,
                selected_country=selected_country,
                selected_region=selected_region,
                output_filename=OUTPUT_PATH
            )
            
            if os.path.exists(OUTPUT_PATH):
                st.success("✅ Executive Briefing compiled and saved successfully to disk storage matrix.")
                
                # Load the raw bytes into memory to serve via download button download pipe
                with open(OUTPUT_PATH, "rb") as f:
                    pdf_bytes = f.read()
                
                st.download_button(
                    label="📥 Download Executive PDF Report File",
                    data=pdf_bytes,
                    file_name=f"GTD_Intelligence_Briefing_{selected_country or selected_region or 'Global'}.pdf",
                    mime="application/pdf",
                    use_container_width=True
                )
            else:
                st.error("❌ Synthesis completed, but report file layout engine failed to locate output file path.")
                
        except Exception as e:
            st.error(f"❌ Document compilation failed unexpectedly: {e}")

# 5. Methodological Safeguard Notice
st.markdown("<br><hr style='border-color:rgba(255,255,255,0.05);'>", unsafe_allow_html=True)
st.warning(
    """
    **⚠️ METHODOLOGICAL SAFEGUARD NOTICE:** The generated PDF documentation consists entirely of rule-based retrospective data summaries 
    collated from historical variance parameters inside the Global Terrorism Database (GTD). 
    
    The resulting reports serve exclusively as explainable decision-support files for academic, historical retrospective review. 
    They do not incorporate dynamic physical real-world data feeds, current political adjustments, or dynamic defensive maneuvers, 
    and **must never** be leveraged to forecast dynamic prospective security elements.
    """
)