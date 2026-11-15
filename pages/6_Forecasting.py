import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
if str(BASE_DIR) not in sys.path:
    sys.path.append(str(BASE_DIR))

import streamlit as st
import plotly.graph_objects as go
from utils.data_loader import load_data
from utils.forecasting import generate_trend_forecast
from utils.dashboard_metrics import render_page_header, render_kpi_card, render_footer

st.set_page_config(
    page_title="Historical Forecasting Dashboard | Threat Intelligence",
    page_icon="📈",
    layout="wide",
)

render_page_header(
    title="📈 Historical Trend Forecasting & Volatility Extrapolation",
    subtitle="Rolling Averages, Linear Regression Trajectory Modeling & ±1σ Historical Volatility Envelopes",
    badge_text="STATISTICAL EXTRAPOLATION",
)

try:
    df = load_data()
except Exception as e:
    st.error(f"❌ Failed to load global dataset: {e}")
    st.stop()

st.sidebar.header("🛠️ Forecast Configuration")
scope_mode = st.sidebar.radio("Geographical Scope", ["Global", "By Region", "By Country"])
region_filter = None
country_filter = None

if scope_mode == "By Region":
    region_filter = st.sidebar.selectbox("Select Region", sorted(df["region_txt"].dropna().unique()))
elif scope_mode == "By Country":
    country_filter = st.sidebar.selectbox("Select Country", sorted(df["country_txt"].dropna().unique()))

metric_choice = st.sidebar.selectbox(
    "Select Metric for Evaluation",
    options=["incident_count", "fatalities", "casualties"],
    format_func=lambda x: x.replace("_", " ").title(),
)

rolling_window = st.sidebar.slider("Rolling Average Window (Years)", min_value=2, max_value=10, value=3, step=1)
forecast_years = st.sidebar.slider("Extrapolation Horizon (Years)", min_value=1, max_value=10, value=5, step=1)

yearly_data, future_df, historical_mean, growth_rate_per_year = generate_trend_forecast(
    df=df,
    metric_choice=metric_choice,
    rolling_window=rolling_window,
    forecast_years=forecast_years,
    country_filter=country_filter,
    region_filter=region_filter,
)

if yearly_data.empty:
    st.error("❌ Processed metrics array came back empty for the selected filter scope.")
    st.stop()

scope_label = country_filter or region_filter or "Global"
st.subheader(f"📊 {metric_choice.replace('_', ' ').title()} Trajectory & Extrapolation — {scope_label}")

fig = go.Figure()

# Observed Historical Data
fig.add_trace(
    go.Scatter(
        x=yearly_data["iyear"],
        y=yearly_data[metric_choice],
        mode="lines+markers",
        name="Observed Historical Data",
        line=dict(color="#3b82f6", width=2.8),
        marker=dict(size=7),
    )
)

# Rolling Average
fig.add_trace(
    go.Scatter(
        x=yearly_data["iyear"],
        y=yearly_data["rolling_avg"],
        mode="lines",
        name=f"{rolling_window}-Year Rolling Average",
        line=dict(color="#10b981", width=2.2, dash="dot"),
    )
)

# Linear Regression Model Fit
fig.add_trace(
    go.Scatter(
        x=yearly_data["iyear"],
        y=yearly_data["trend_line"],
        mode="lines",
        name="Linear Regression Fit",
        line=dict(color="rgba(245, 158, 11, 0.7)", width=2),
    )
)

# Volatility Confidence Band (±1σ)
if "upper_bound" in future_df.columns and "lower_bound" in future_df.columns:
    fig.add_trace(
        go.Scatter(
            x=list(future_df["iyear"]) + list(future_df["iyear"][::-1]),
            y=list(future_df["upper_bound"]) + list(future_df["lower_bound"][::-1]),
            fill="toself",
            fillcolor="rgba(239, 68, 68, 0.15)",
            line=dict(color="rgba(255,255,255,0)"),
            hoverinfo="skip",
            showlegend=True,
            name="±1σ Volatility Envelope",
        )
    )

# Extrapolated Segment
fig.add_trace(
    go.Scatter(
        x=future_df["iyear"],
        y=future_df["trend_line"],
        mode="lines+markers",
        name="Statistical Trend Extrapolation",
        line=dict(color="#ef4444", width=2.8, dash="dash"),
        marker=dict(symbol="diamond", size=7),
    )
)

fig.update_layout(
    template="plotly_dark",
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(15, 23, 42, 0.5)",
    margin=dict(l=40, r=40, t=30, b=40),
    hovermode="x unified",
    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
    xaxis=dict(title="Timeline (Years)", gridcolor="rgba(255,255,255,0.05)"),
    yaxis=dict(title="Volume Scale", gridcolor="rgba(255,255,255,0.05)"),
)

st.plotly_chart(fig, width='stretch')

st.subheader("💡 Analytical Insights & Progression Rate")
col1, col2, col3 = st.columns(3)

with col1:
    render_kpi_card("Historical Annual Mean", f"{historical_mean:,.1f}", f"Scope: {scope_label}", "#3b82f6")
with col2:
    direction = "Upward Shift" if growth_rate_per_year > 0 else "Downward Decay"
    render_kpi_card("Year-over-Year Slope", direction, f"{growth_rate_per_year:+.2f} units / yr", "#f59e0b")
with col3:
    max_year = int(yearly_data["iyear"].max())
    projected_end_val = float(future_df["trend_line"].iloc[-1])
    render_kpi_card(
        f"Projected Year-{max_year + forecast_years} Baseline",
        f"{projected_end_val:,.1f}",
        f"{forecast_years}-Year Linear Extrapolation",
        "#ef4444",
    )

render_footer(
    "**⚠️ METHODOLOGICAL SAFEGUARD NOTICE:** The trend lines and projections displayed on this dashboard represent purely mathematical "
    "extrapolations (Linear Regression and Rolling Means) derived from historical variance across the GTD. "
    "They must not be interpreted as actionable prognostic forecasts of real-world security events."
)
