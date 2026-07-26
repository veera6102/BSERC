import plotly.express as px

def line_chart(df, x_col, y_col, title="Line Chart"):
    """
    Generates a uniform dark-themed line chart.
    """
    fig = px.line(
        df, 
        x=x_col, 
        y=y_col, 
        title=title,
        template="plotly_dark"
    )
    fig.update_layout(
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        xaxis=dict(showgrid=False),
        yaxis=dict(showgrid=True, gridcolor="rgba(255,255,255,0.1)")
    )
    return fig

def bar_chart(df, x_col, y_col, title="Bar Chart", orientation="v"):
    """
    Generates a uniform dark-themed bar chart.
    """
    fig = px.bar(
        df, 
        x=x_col if orientation == "v" else y_col, 
        y=y_col if orientation == "v" else x_col, 
        title=title,
        orientation=orientation,
        template="plotly_dark"
    )
    fig.update_layout(
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        xaxis=dict(showgrid=False if orientation == "v" else True, gridcolor="rgba(255,255,255,0.1)"),
        yaxis=dict(showgrid=True if orientation == "v" else False, gridcolor="rgba(255,255,255,0.1)")
    )
    return fig