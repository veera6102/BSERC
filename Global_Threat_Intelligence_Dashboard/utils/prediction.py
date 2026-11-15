import sys
from pathlib import Path

# ==============================================================================
# 1. PATH RESOLUTION INJECTION (Must stand before custom local imports)
# ==============================================================================
BASE_DIR = Path(__file__).resolve().parent.parent
if str(BASE_DIR) not in sys.path:
    sys.path.append(str(BASE_DIR))

# ==============================================================================
# 2. APPLICATION IMPORTS
# ==============================================================================
import streamlit as st
import joblib
import pandas as pd
import numpy as np
from config import ATTACK_MODEL_PATH, MODEL_DIR
from utils.data_loader import load_data

# Define metric paths for model dictionaries
FEATURE_ENCODER_PATH = MODEL_DIR / "feature_encoders.pkl"
TARGET_ENCODER_PATH = MODEL_DIR / "target_encoder.pkl"

# ==============================================================================
# 3. INTERACTIVE PREDICTION INTERFACE
# ==============================================================================
def main():
    st.title("🔮 Tactical Attack Type Modeler")
    st.markdown("Supply operational threat metrics below to simulate adversarial tendencies and predict incident method profiles.")
    st.markdown("---")

    # 1. Verification Guardrail Check for Calibrated Binaries
    if not (ATTACK_MODEL_PATH.exists() and FEATURE_ENCODER_PATH.exists() and TARGET_ENCODER_PATH.exists()):
        st.warning("⚠️ Predictive Intelligence System Offline.")
        st.info("Please complete the core machine learning training execution parameters on your dashboard homepage first.")
        return

    # 2. Load Models and Mappers Artifacts from storage
    @st.cache_resource
    def load_prediction_artifacts():
        model = joblib.load(ATTACK_MODEL_PATH)
        feature_encoders = joblib.load(FEATURE_ENCODER_PATH)
        target_encoder = joblib.load(TARGET_ENCODER_PATH)
        return model, feature_encoders, target_encoder

    model, feature_encoders, target_encoder = load_prediction_artifacts()
    
    # Load underlying base data frameworks to populate dropdown options safely
    df = load_data()

    # 3. Structural Grid Input Formulation
    st.subheader("🕵️ Scenario Input Parameters Configuration")
    
    col1, col2 = st.columns(2)
    
    with col1:
        selected_country = st.selectbox("Target Jurisdiction (Country)", sorted(df["country_txt"].dropna().unique()))
        selected_region = st.selectbox("Geographic Focus (Region)", sorted(df["region_txt"].dropna().unique()))
        selected_target = st.selectbox("Target Classification Sector", sorted(df["targtype1_txt"].dropna().unique()))
        selected_weapon = st.selectbox("Primary Intended Weapon Class", sorted(df["weaptype1_txt"].dropna().unique()))

    with col2:
        selected_year = st.slider("Simulated Operational Timeline (Year)", int(df["iyear"].min()), 2030, 2026)
        is_success = st.selectbox("Historical Mission Success Condition", [1, 0], format_func=lambda x: "Success Case (1)" if x == 1 else "Failure Case (0)")
        is_suicide = st.selectbox("Tactical Mode (Suicide Operational Design)", [0, 1], format_func=lambda x: "Standard Mode (0)" if x == 0 else "Suicide Operational Mission (1)")

    st.markdown("---")

    # 4. Processing Inference Executions
    if st.button("🚀 Execute Predictive Inference Simulation", use_container_width=True):
        with st.spinner("Processing scenario matrix arrays through champion classifier layer..."):
            try:
                # Structure raw interactive strings into DataFrame matching training shapes
                input_data = pd.DataFrame([{
                    "country_txt": selected_country,
                    "region_txt": selected_region,
                    "targtype1_txt": selected_target,
                    "weaptype1_txt": selected_weapon,
                    "iyear": selected_year,
                    "success": is_success,
                    "suicide": is_suicide
                }])

                # Apply mapping sequences safely using pre-computed label encoders
                for col in input_data.columns:
                    if col in feature_encoders:
                        le = feature_encoders[col]
                        val_str = str(input_data.loc[0, col])
                        # Handle potential unseen labels smoothly
                        if val_str in le.classes_:
                            input_data.loc[0, col] = le.transform([val_str])[0]
                        else:
                            input_data.loc[0, col] = 0  # Fallback vector index

                # Extract probabilities arrays
                probabilities = model.predict_proba(input_data)[0]
                classes = target_encoder.classes_

                # Identify champion prediction choice
                highest_idx = np.argmax(probabilities)
                predicted_class = classes[highest_idx]
                highest_prob = probabilities[highest_idx]

                # 5. Presentation Layer Outputs
                st.success(f"### 🎯 Predicted Tactical Profile Target Strategy: **{predicted_class}**")
                st.metric(label="Model Predictive Confidence Vector Strength", value=f"{highest_prob:.2%}")
                
                # Breakdown detailed probabilities table
                st.markdown("#### Complete Model Probabilities Vector Array Breakdown")
                prob_df = pd.DataFrame({
                    "Tactical Method Mode": classes,
                    "Predictive Probability Distribution": probabilities
                }).sort_values(by="Predictive Probability Distribution", ascending=False).reset_index(drop=True)
                
                # Format formatting visual displays style metrics
                prob_df["Predictive Probability Distribution"] = prob_df["Predictive Probability Distribution"].map(lambda x: f"{x:.2%}")
                st.dataframe(prob_df, use_container_width=True)

            except Exception as e:
                st.error(f"❌ Structural Simulation Exception Encountered: {e}")

if __name__ == "__main__":
    main()