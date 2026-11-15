import joblib
import numpy as np
import pandas as pd
import streamlit as st
from config import (
    ATTACK_MODEL_PATH,
    FEATURE_ENCODER_PATH,
    TARGET_ENCODER_PATH,
)


def models_are_ready() -> bool:
    """Checks whether all required ML prediction artifacts exist on disk."""
    return (
        ATTACK_MODEL_PATH.exists()
        and FEATURE_ENCODER_PATH.exists()
        and TARGET_ENCODER_PATH.exists()
    )


@st.cache_resource(show_spinner=False)
def load_prediction_artifacts():
    """Loads and caches the trained classifier and categorical encoders."""
    model = joblib.load(ATTACK_MODEL_PATH)
    feature_encoders = joblib.load(FEATURE_ENCODER_PATH)
    target_encoder = joblib.load(TARGET_ENCODER_PATH)
    return model, feature_encoders, target_encoder


def predict_attack_profile(
    country_txt: str,
    region_txt: str,
    targtype1_txt: str,
    weaptype1_txt: str,
    iyear: int,
    success: int,
    suicide: int,
):
    """
    Runs inference on a single tactical scenario and returns:
    (predicted_class, highest_prob, prob_df)
    """
    model, feature_encoders, target_encoder = load_prediction_artifacts()

    raw_values = {
        "country_txt": country_txt,
        "region_txt": region_txt,
        "targtype1_txt": targtype1_txt,
        "weaptype1_txt": weaptype1_txt,
        "iyear": int(iyear),
        "success": int(success),
        "suicide": int(suicide),
    }

    encoded_row = {}
    for col, val in raw_values.items():
        if col in feature_encoders:
            le = feature_encoders[col]
            val_str = str(val)
            if val_str in le.classes_:
                encoded_row[col] = int(le.transform([val_str])[0])
            else:
                encoded_row[col] = 0
        else:
            encoded_row[col] = int(val)

    input_data = pd.DataFrame([encoded_row])

    probabilities = model.predict_proba(input_data)[0]
    classes = target_encoder.classes_

    highest_idx = int(np.argmax(probabilities))
    predicted_class = str(classes[highest_idx])
    highest_prob = float(probabilities[highest_idx])

    prob_df = (
        pd.DataFrame(
            {
                "Tactical Method Mode": classes,
                "Probability": probabilities,
            }
        )
        .sort_values(by="Probability", ascending=False)
        .reset_index(drop=True)
    )
    prob_df["Confidence (%)"] = prob_df["Probability"].map(lambda x: f"{x:.2%}")

    return predicted_class, highest_prob, prob_df


def find_historical_analogues(
    df: pd.DataFrame,
    country_txt: str,
    targtype1_txt: str,
    weaptype1_txt: str,
    limit: int = 10,
) -> pd.DataFrame:
    """Finds real historical incidents matching the simulated tactical scenario."""
    if df is None or df.empty:
        return pd.DataFrame()

    exact = df[
        (df["country_txt"] == country_txt)
        & (df["targtype1_txt"] == targtype1_txt)
        & (df["weaptype1_txt"] == weaptype1_txt)
    ]
    if len(exact) >= 3:
        subset = exact
    else:
        subset = df[
            (df["targtype1_txt"] == targtype1_txt)
            & (df["weaptype1_txt"] == weaptype1_txt)
        ]

    cols = [
        c
        for c in [
            "iyear",
            "country_txt",
            "city",
            "gname",
            "attacktype1_txt",
            "targtype1_txt",
            "weaptype1_txt",
            "nkill",
            "nwound",
            "success",
        ]
        if c in subset.columns
    ]
    return subset[cols].sort_values(by="iyear", ascending=False).head(limit)
