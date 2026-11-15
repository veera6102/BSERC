import streamlit as st
import plotly.graph_objects as go
from utils.data_loader import load_data
from utils.forecasting import generate_trend_forecast

# 1. Page Configuration
st.set_page_config(
    page_title="Historical Forecasting Dashboard | Threat Intelligence",
    page_icon="📈",
    layout="wide"
)

st.markdown("<h1 class='glow-text'>📈 Historical Trend Forecasting & Extrapolation</h1>", unsafe_allow_html=True)
st.markdown("<p style='color:#94a3b8;font-size:1.1rem;'>Statistical Extrapolations, Rolling Averages, and Volatility Indicators based on Historical Patterns.</p>", unsafe_allow_html=True)
st.markdown("<hr style='border-color:rgba(59, 130, 246, 0.2);'>", unsafe_allow_html=True)

# 2. Safely Load Data Pipeline
try:
    df = load_data()
except Exception as e:
    st.error(f"❌ Failed to load global dataset: {e}")
    st.stop()

# 3. Sidebar Configuration Controls
st.sidebar.header("🛠️ Forecast Configuration")
metric_choice = st.sidebar.selectbox(
    "Select Metric for Evaluation",
    options=["incident_count", "fatalities", "casualties"],
    format_func=lambda x: x.replace("_", " ").title()
)

rolling_window = st.sidebar.slider(
    "Rolling Average Window (Years)", 
    min_value=2, max_value=10, value=5, step=1
)

forecast_years = st.sidebar.slider(
    "Extrapolation Horizon (Years past max data)", 
    min_value=1, max_value=10, value=5, step=1
)

# 4. Process Computations via Decoupled Backend Utility
yearly_data, future_df, historical_mean, growth_rate_per_year = generate_trend_forecast(
    df=df,
    metric_choice=metric_choice,
    rolling_window=rolling_window,
    forecast_years=forecast_years
)

if yearly_data.empty:
    st.error("❌ Processed metrics array came back empty. Verify dataset date columns.")
    st.stop()

# 5. Interactive Visualization View Layer
st.subheader(f"📊 {metric_choice.replace('_', ' ').title()} Progression & Extrapolation Baseline")

fig = go.Figure()

# Historical Observed values
fig.add_trace(go.Scatter(
    x=yearly_data['iyear'], y=yearly_data[metric_choice],
    mode='lines+markers', name='Observed Historical Data',
    line=dict(color='#3b82f6', width=2.5),
    marker=dict(size=6)
))

# Rolling Average
fig.add_trace(go.Scatter(
    x=yearly_data['iyear'], y=yearly_data['rolling_avg'],
    mode='lines', name=f'{rolling_window}-Year Rolling Average',
    line=dict(color='#10b981', width=2, dash='dot')
))

# Linear Regression Model Fit (Historical)
fig.add_trace(go.Scatter(
    x=yearly_data['iyear'], y=yearly_data['trend_line'],
    mode='lines', name='Historical Growth/Decay Rate',
    line=dict(color='rgba(245, 158, 11, 0.5)', width=2)
))

# Extrapolated Segment (Future Projection Base)
fig.add_trace(go.Scatter(
    x=future_df['iyear'], y=future_df['trend_line'],
    mode='lines+markers', name='Statistical Trend Extrapolation',
    line=dict(color='#ef4444', width=2.5, dash='dash'),
    marker=dict(symbol='diamond', size=6)
))

# Dark theme structural styles
fig.update_layout(
    template="plotly_dark",
    paper_bgcolor="rgba(0,0,0,0)",     # CORRECTED: Changed from background_color to paper_bgcolor for outer area transparency
    plot_bgcolor="rgba(15, 23, 42, 0.5)", # Sets background color inside the grid lines area
    margin=dict(l=40, r=40, t=20, b=40),
    hovermode="x unified",
    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
    xaxis=dict(title="Timeline (Years)", gridcolor="rgba(255,255,255,0.05)"),
    yaxis=dict(title="Volume Scale", gridcolor="rgba(255,255,255,0.05)")
)

st.plotly_chart(fig, use_container_width=True)

# 6. Structured Scorecards Overview
st.subheader("💡 Analytical Insights & Progression Rate")
col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        label="Historical Database Average", 
        value=f"{historical_mean:,.2f}",
        help="The overall historical mean calculated across all evaluated years."
    )
with col2:
    st.metric(
        label="Calculated Year-over-Year Trajectory", 
        value="Upward Shift" if growth_rate_per_year > 0 else "Downward Decay",
        delta=f"{growth_rate_per_year:+.2f} units / yr",
        help="The average mathematical trajectory movement calculated per timeline year step."
    )
with col3:
    max_year = int(yearly_data['iyear'].max())
    projected_end_val = future_df['trend_line'].iloc[-1]
    st.metric(
        label=f"Projected Year-{max_year + forecast_years} Line Target", 
        value=f"{projected_end_val:,.1f}",
        help="The final coordinate value calculated at the terminus edge of the trend projection line."
    )

# 7. Safeguard Disclaimer Notice
st.markdown("<br><hr style='border-color:rgba(255,255,255,0.05);'>", unsafe_allow_html=True)
st.warning(
    """
    **⚠️ METHODOLOGICAL SAFEGUARD NOTICE:** The trend lines and projections displayed on this dashboard represent purely mathematical 
    extrapolations (Linear Regression and Rolling Means) derived entirely from historical variance across the Global Terrorism Database (GTD). 
    
    These projections serve exclusively to identify macroscopic historical data patterns and long-term research trends. They do not incorporate 
    dynamic real-world geopolitics, defense counter-measures, or active physical intelligence factors, and **must not** be interpreted as actionable 
    prognostic forecasts of prospective kinetic threats or real-world security events.
    """
)