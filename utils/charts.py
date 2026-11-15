import plotly.express as px
import plotly.graph_objects as go


def line_chart(df, x_col, y_col, title="Line Chart", color="#3b82f6"):
    """Generates a uniform dark-themed area/line chart with glowing markers."""
    fig = px.area(
        df,
        x=x_col,
        y=y_col,
        title=title,
        markers=True,
        template="plotly_dark",
    )
    fig.update_traces(
        line=dict(color=color, width=3),
        fillcolor="rgba(59, 130, 246, 0.14)",
        marker=dict(size=6, color="#ef4444", line=dict(width=1, color="#ffffff")),
    )
    fig.update_layout(
        plot_bgcolor="rgba(15, 23, 42, 0.45)",
        paper_bgcolor="rgba(0,0,0,0)",
        margin=dict(l=30, r=30, t=45, b=30),
        hovermode="x unified",
        xaxis=dict(showgrid=False),
        yaxis=dict(showgrid=True, gridcolor="rgba(255,255,255,0.07)"),
    )
    return fig


def bar_chart(df, x_col, y_col, title="Bar Chart", orientation="v", color_scale="Blues"):
    """Generates a uniform dark-themed gradient bar chart."""
    fig = px.bar(
        df,
        x=x_col if orientation == "v" else y_col,
        y=y_col if orientation == "v" else x_col,
        title=title,
        orientation=orientation,
        color=y_col,
        color_continuous_scale=color_scale,
        template="plotly_dark",
    )
    fig.update_layout(
        plot_bgcolor="rgba(15, 23, 42, 0.45)",
        paper_bgcolor="rgba(0,0,0,0)",
        margin=dict(l=30, r=30, t=45, b=30),
        coloraxis_showscale=False,
        xaxis=dict(
            showgrid=False if orientation == "v" else True,
            gridcolor="rgba(255,255,255,0.07)",
        ),
        yaxis=dict(
            showgrid=True if orientation == "v" else False,
            gridcolor="rgba(255,255,255,0.07)",
            categoryorder="total ascending" if orientation == "h" else "trace",
        ),
    )
    return fig


def donut_chart(df, names_col, values_col, title="Distribution"):
    """Generates a sleek dark-themed donut chart."""
    fig = px.pie(
        df,
        names=names_col,
        values=values_col,
        title=title,
        hole=0.58,
        template="plotly_dark",
        color_discrete_sequence=px.colors.sequential.Blues_r,
    )
    fig.update_traces(textposition="inside", textinfo="percent+label")
    fig.update_layout(
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        margin=dict(l=20, r=20, t=45, b=20),
        showlegend=True,
    )
    return fig


def risk_gauge_chart(score: float, level: str):
    """Generates a 0-120 speedometer gauge chart for the Threat Level Calculator."""
    color_map = {
        "LOW": "#10b981",
        "MODERATE": "#f59e0b",
        "HIGH": "#f97316",
        "CRITICAL": "#ef4444",
    }
    bar_color = color_map.get(level, "#3b82f6")

    fig = go.Figure(
        go.Indicator(
            mode="gauge+number",
            value=score,
            number={"suffix": " / 120", "font": {"size": 34, "color": "#f8fafc"}},
            title={"text": f"Threat Classification: <b>{level}</b>", "font": {"size": 16, "color": "#94a3b8"}},
            gauge={
                "axis": {"range": [0, 120], "tickwidth": 1, "tickcolor": "#64748b"},
                "bar": {"color": bar_color, "thickness": 0.32},
                "bgcolor": "rgba(15, 23, 42, 0.7)",
                "borderwidth": 1,
                "bordercolor": "rgba(148, 163, 184, 0.2)",
                "steps": [
                    {"range": [0, 35], "color": "rgba(16, 185, 129, 0.18)"},
                    {"range": [35, 65], "color": "rgba(245, 158, 11, 0.18)"},
                    {"range": [65, 85], "color": "rgba(249, 115, 22, 0.20)"},
                    {"range": [85, 120], "color": "rgba(239, 68, 68, 0.24)"},
                ],
                "threshold": {
                    "line": {"color": "#ffffff", "width": 3},
                    "thickness": 0.8,
                    "value": score,
                },
            },
        )
    )
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font={"color": "#f1f5f9"},
        height=300,
        margin=dict(l=30, r=30, t=50, b=20),
    )
    return fig
