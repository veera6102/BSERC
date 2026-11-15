import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
if str(BASE_DIR) not in sys.path:
    sys.path.append(str(BASE_DIR))

import streamlit as st
import plotly.express as px
from utils.data_loader import load_data
from utils.prediction import (
    models_are_ready,
    predict_attack_profile,
    find_historical_analogues,
)
from utils.dashboard_metrics import render_page_header, render_kpi_card, render_footer

st.set_page_config(
    page_title="Attack Prediction Modeler | Threat Intelligence",
    page_icon="🔮",
    layout="wide",
)

render_page_header(
    title="🔮 Tactical Attack Type Modeler",
    subtitle="Multi-Class XGBoost Scenario Simulator, Probability Distribution & Historical Precedent Matcher",
    badge_text="ML INFERENCE ENGINE",
)


def main():
    if not models_are_ready():
        st.warning("⚠️ Predictive Intelligence System Offline.")
        st.info("Please initialize or recalibrate the ML models from the Command Center homepage first.")
        return

    df = load_data()

    st.subheader("🕵️ Scenario Input Parameters Configuration")
    col1, col2 = st.columns(2)

    with col1:
        countries = sorted(df["country_txt"].dropna().unique().tolist())
        selected_country = st.selectbox("Target Jurisdiction (Country)", countries)

        # Auto-resolve the country's region as the default selection
        country_regions = df[df["country_txt"] == selected_country]["region_txt"].dropna().unique().tolist()
        all_regions = sorted(df["region_txt"].dropna().unique().tolist())
        default_reg_idx = all_regions.index(country_regions[0]) if country_regions and country_regions[0] in all_regions else 0

        selected_region = st.selectbox("Geographic Focus (Region)", all_regions, index=default_reg_idx)
        selected_target = st.selectbox("Target Classification Sector", sorted(df["targtype1_txt"].dropna().unique()))
        selected_weapon = st.selectbox("Primary Intended Weapon Class", sorted(df["weaptype1_txt"].dropna().unique()))

    with col2:
        selected_year = st.slider("Simulated Operational Timeline (Year)", int(df["iyear"].min()), 2030, 2026)
        is_success = st.selectbox(
            "Historical Mission Success Condition",
            [1, 0],
            format_func=lambda x: "Success Case (1)" if x == 1 else "Failure Case (0)",
        )
        is_suicide = st.selectbox(
            "Tactical Mode (Suicide Operational Design)",
            [0, 1],
            format_func=lambda x: "Standard Mode (0)" if x == 0 else "Suicide Operational Mission (1)",
        )

    st.markdown("<br>", unsafe_allow_html=True)

    if st.button("🚀 Execute Predictive Inference Simulation", type="primary", width='stretch'):
        with st.spinner("Processing scenario vector through calibrated XGBoost classifier..."):
            try:
                predicted_class, highest_prob, prob_df = predict_attack_profile(
                    country_txt=selected_country,
                    region_txt=selected_region,
                    targtype1_txt=selected_target,
                    weaptype1_txt=selected_weapon,
                    iyear=selected_year,
                    success=is_success,
                    suicide=is_suicide,
                )

                res1, res2, res3 = st.columns(3)
                with res1:
                    render_kpi_card("Predicted Tactical Vector", predicted_class, f"Jurisdiction: {selected_country}", "#10b981")
                with res2:
                    render_kpi_card("Classifier Confidence", f"{highest_prob:.2%}", "Top Class Probability", "#3b82f6")
                with res3:
                    runner_up = prob_df.iloc[1]["Tactical Method Mode"] if len(prob_df) > 1 else "N/A"
                    runner_prob = prob_df.iloc[1]["Confidence (%)"] if len(prob_df) > 1 else "0%"
                    render_kpi_card("Secondary Alternative Vector", str(runner_up), f"Secondary Confidence: {runner_prob}", "#f59e0b")

                chart_col, table_col = st.columns([1.3, 1])
                with chart_col:
                    fig_prob = px.bar(
                        prob_df.sort_values(by="Probability", ascending=True),
                        x="Probability",
                        y="Tactical Method Mode",
                        orientation="h",
                        title="Multi-Class Probability Distribution",
                        color="Probability",
                        color_continuous_scale="Blugrn",
                        template="plotly_dark",
                    )
                    fig_prob.update_layout(
                        paper_bgcolor="rgba(0,0,0,0)",
                        plot_bgcolor="rgba(15, 23, 42, 0.5)",
                        coloraxis_showscale=False,
                        xaxis_tickformat=".0%",
                    )
                    st.plotly_chart(fig_prob, width='stretch')

                with table_col:
                    st.markdown("#### Complete Probability Breakdown")
                    st.dataframe(
                        prob_df[["Tactical Method Mode", "Confidence (%)"]],
                        width='stretch',
                        hide_index=True,
                    )

                # Historical Analogues Lookup
                st.markdown("---")
                st.subheader("🔎 Historical Analogous Precedents in GTD")
                analogues = find_historical_analogues(
                    df=df,
                    country_txt=selected_country,
                    targtype1_txt=selected_target,
                    weaptype1_txt=selected_weapon,
                )
                if not analogues.empty:
                    st.caption("Real historical GTD incidents matching your selected Target and Weapon parameters:")
                    st.dataframe(analogues, width='stretch', hide_index=True)
                else:
                    st.info("No exact historical analogues found for this specific combination.")

            except Exception as e:
                st.error(f"❌ Structural Simulation Exception Encountered: {e}")

    render_footer(
        "**⚠️ ML INFERENCE DISCLAIMER:** Predictions reflect statistical class probabilities learned from historical GTD records "
        "and must never be used as operational forecasts of real-world events."
    )


if __name__ == "__main__":
    main()
