import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression

def generate_trend_forecast(df, metric_choice="incident_count", rolling_window=5, forecast_years=5):
    """
    Handles background data aggregation, rolling average calculation, 
    and linear trend extrapolation for the dashboard metrics.
    """
    # 1. Cleanly aggregate target metrics by year
    if 'nkill' not in df.columns or 'nwound' not in df.columns:
        df['total_casualties'] = 0
    else:
        df['total_casualties'] = df['nkill'].fillna(0) + df['nwound'].fillna(0)

    yearly_data = df.groupby('iyear').agg(
        incident_count=('eventid', 'count'),
        fatalities=('nkill', 'sum'),
        casualties=('total_casualties', 'sum')
    ).reset_index()

    # Align with historical timeline boundaries
    yearly_data = yearly_data[(yearly_data['iyear'] >= 1970) & (yearly_data['iyear'] <= 2020)]

    if yearly_data.empty:
        return pd.DataFrame(), pd.DataFrame(), 0, 0

    # 2. Compute Rolling Window Statistics
    yearly_data['rolling_avg'] = yearly_data[metric_choice].rolling(window=rolling_window, min_periods=1).mean()

    # 3. Fit Linear Model over Observed Target Array
    X_hist = yearly_data['iyear'].values.reshape(-1, 1)
    y_hist = yearly_data[metric_choice].values

    lr_model = LinearRegression()
    lr_model.fit(X_hist, y_hist)
    yearly_data['trend_line'] = lr_model.predict(X_hist)

    # 4. Generate Future Linear Extrapolation Sequence
    max_year = int(yearly_data['iyear'].max())
    future_years = np.array(range(max_year + 1, max_year + 1 + forecast_years)).reshape(-1, 1)
    future_preds = lr_model.predict(future_years)

    # Enforce realistic mathematical baseline boundary floors (no negative volumes)
    future_preds = np.clip(future_preds, a_min=0, a_max=None)

    future_df = pd.DataFrame({
        'iyear': future_years.flatten(),
        'trend_line': future_preds
    })

    # Historical average and the baseline slope coefficient metric
    historical_mean = yearly_data[metric_choice].mean()
    growth_rate_per_year = lr_model.coef_[0]

    return yearly_data, future_df, historical_mean, growth_rate_per_year