import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression


def generate_trend_forecast(
    df,
    metric_choice="incident_count",
    rolling_window=5,
    forecast_years=5,
    country_filter=None,
    region_filter=None,
):
    """
    Handles background data aggregation, rolling average calculation,
    and linear trend extrapolation for the dashboard metrics.
    """
    work_df = df.copy()

    if country_filter and country_filter != "All" and "country_txt" in work_df.columns:
        work_df = work_df[work_df["country_txt"] == country_filter]
    elif region_filter and region_filter != "All" and "region_txt" in work_df.columns:
        work_df = work_df[work_df["region_txt"] == region_filter]

    if "nkill" not in work_df.columns or "nwound" not in work_df.columns:
        work_df["total_casualties"] = 0
    else:
        work_df["total_casualties"] = work_df["nkill"].fillna(0) + work_df["nwound"].fillna(0)

    yearly_data = (
        work_df.groupby("iyear")
        .agg(
            incident_count=("eventid", "count"),
            fatalities=("nkill", "sum"),
            casualties=("total_casualties", "sum"),
        )
        .reset_index()
    )

    yearly_data = yearly_data[(yearly_data["iyear"] >= 1970) & (yearly_data["iyear"] <= 2025)]

    if yearly_data.empty:
        return pd.DataFrame(), pd.DataFrame(), 0.0, 0.0

    # Compute Rolling Window Statistics
    yearly_data["rolling_avg"] = (
        yearly_data[metric_choice].rolling(window=rolling_window, min_periods=1).mean()
    )

    # Fit Linear Model over Observed Target Array
    X_hist = yearly_data["iyear"].values.reshape(-1, 1)
    y_hist = yearly_data[metric_choice].values

    lr_model = LinearRegression()
    lr_model.fit(X_hist, y_hist)
    yearly_data["trend_line"] = lr_model.predict(X_hist)

    # Residual standard deviation for volatility band
    residuals = y_hist - yearly_data["trend_line"].values
    std_err = float(np.std(residuals)) if len(residuals) > 1 else float(np.mean(y_hist) * 0.1)

    # Generate Future Linear Extrapolation Sequence
    max_year = int(yearly_data["iyear"].max())
    future_years = np.array(range(max_year + 1, max_year + 1 + forecast_years)).reshape(-1, 1)
    future_preds = np.clip(lr_model.predict(future_years), a_min=0, a_max=None)

    future_df = pd.DataFrame(
        {
            "iyear": future_years.flatten(),
            "trend_line": future_preds,
            "upper_bound": np.clip(future_preds + std_err, a_min=0, a_max=None),
            "lower_bound": np.clip(future_preds - std_err, a_min=0, a_max=None),
        }
    )

    historical_mean = float(yearly_data[metric_choice].mean())
    growth_rate_per_year = float(lr_model.coef_[0])

    return yearly_data, future_df, historical_mean, growth_rate_per_year
