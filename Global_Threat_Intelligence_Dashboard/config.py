import os

# --- Dynamic Core Platform Paths ---
# Calculates the absolute workspace root directory dynamically
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

DATA_PATH = os.path.join(BASE_DIR, "data", "globalterrorism.csv")
PREDICTION_MODEL_PATH = os.path.join(BASE_DIR, "models", "attack_prediction_model.pkl")
RISK_MODEL_PATH = os.path.join(BASE_DIR, "models", "risk_model.pkl")
METRICS_JSON_PATH = os.path.join(BASE_DIR, "models", "metrics.json")

# --- UI Custom Theme & Typography Frameworks (Fixes the ImportError) ---
CSS_STYLE = """
<style>
    /* Global Dashboard Dark UI Background Canvas */
    .stApp {
        background-color: #0f172a;
        color: #f1f5f9;
    }
    
    /* Blue Neon Glow Title Accentuation Header */
    .glow-text {
        color: #3b82f6;
        text-shadow: 0 0 12px rgba(59, 130, 246, 0.4);
        font-weight: 700;
        margin-top: 5px;
    }
    
    /* High-Contrast Border Cards for Core Summary Components */
    .kpi-card {
        background-color: rgba(15, 23, 42, 0.6);
        border: 1px solid rgba(59, 130, 246, 0.15);
        border-radius: 8px;
        padding: 20px;
        margin-bottom: 15px;
    }
    
    /* Standardized Footer container structural formatting layout */
    .footer-container {
        text-align: center; 
        margin-top: 40px; 
        padding: 20px; 
        color: #64748b; 
        font-size: 0.85rem;
        border-top: 1px solid rgba(255,255,255,0.05);
    }
</style>
"""