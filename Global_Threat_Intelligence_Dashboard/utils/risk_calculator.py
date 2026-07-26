import pandas as pd
import numpy as np

def compute_data_driven_weights(df):
    """
    Dynamically computes weights for weapons and targets based on historical GTD data.
    Normalizes the average casualties (kills + wounds) to a 0-40 scale.
    """
    # Create a total casualties column if it doesn't exist
    if 'nkill' in df.columns and 'nwound' in df.columns:
        df['total_casualties'] = df['nkill'].fillna(0) + df['nwound'].fillna(0)
    else:
        df['total_casualties'] = 0

    # 1. Compute Weapon Scores
    weapon_stats = df.groupby('weaptype1_txt')['total_casualties'].mean().to_dict()
    max_weap_avg = max(weapon_stats.values()) if weapon_stats and max(weapon_stats.values()) > 0 else 1
    # Normalize to 0-40 scale, minimum baseline score of 10
    weapon_scores = {k: int(10 + (v / max_weap_avg) * 30) for k, v in weapon_stats.items()}

    # 2. Compute Target Scores
    target_stats = df.groupby('targtype1_txt')['total_casualties'].mean().to_dict()
    max_targ_avg = max(target_stats.values()) if target_stats and max(target_stats.values()) > 0 else 1
    # Normalize to 0-40 scale, minimum baseline score of 10
    target_scores = {k: int(10 + (v / max_targ_avg) * 30) for k, v in target_stats.items()}

    return weapon_scores, target_scores


def calculate_risk(weapon, target, success, suicide, casualties, df=None):
    """
    Calculates a transparent risk score and corresponding threat level.
    Uses data-driven scoring if a DataFrame is provided, otherwise falls back to standard baselines.
    """
    score = 0
    reasons = []

    # Fallback default configurations if no DataFrame is passed
    DEFAULT_WEAPON_SCORE = {
        "Biological": 40, "Chemical": 35, "Explosives": 30, 
        "Firearms": 25, "Incendiary": 20, "Melee": 10
    }
    DEFAULT_TARGET_SCORE = {
        "Military": 30, "Police": 25, "Government": 20, 
        "Private Citizens & Property": 15, "Business": 10
    }

    # Extract or compute scores
    if df is not None and not df.empty:
        try:
            weapon_scores, target_scores = compute_data_driven_weights(df)
            weapon_weight = weapon_scores.get(weapon, 15)
            target_weight = target_scores.get(target, 15)
            basis_type = "Data-driven"
        except Exception:
            weapon_weight = DEFAULT_WEAPON_SCORE.get(weapon, 15)
            target_weight = DEFAULT_TARGET_SCORE.get(target, 15)
            basis_type = "Baseline"
    else:
        weapon_weight = DEFAULT_WEAPON_SCORE.get(weapon, 15)
        target_weight = DEFAULT_TARGET_SCORE.get(target, 15)
        basis_type = "Baseline"

    # 1. Weapon Score Impact
    score += weapon_weight
    reasons.append(f"Weapon Impact ({weapon}) [{basis_type}]: +{weapon_weight}")

    # 2. Target Score Impact
    score += target_weight
    reasons.append(f"Target Vulnerability ({target}) [{basis_type}]: +{target_weight}")

    # 3. Success Status Impact
    if success == 1:
        score += 10
        reasons.append("Successful Incident Mechanics: +10")

    # 4. Tactical Intent (Suicide Attack)
    if suicide == 1:
        score += 15
        reasons.append("High-Intensity Tactical Profile (Suicide Attack): +15")

    # 5. Severity Metrics (Casualties Impact)
    if casualties >= 50:
        score += 30
        reasons.append("Mass-Casualty Threshold Met (>= 50): +30")
    elif casualties >= 20:
        score += 20
        reasons.append("Elevated Casualty Scale Met (>= 20): +20")
    elif casualties >= 10:
        score += 10
        reasons.append("Moderate Casualty Scale Met (>= 10): +10")
    elif casualties > 0:
        score += 5
        reasons.append("Minor Casualty Scale Impact (> 0): +5")

    # 6. Determine Final Normalized Threat Level Classification
    if score < 35:
        level = "LOW"
    elif score < 65:
        level = "MODERATE"
    elif score < 85:
        level = "HIGH"
    else:
        level = "CRITICAL"

    return score, level, reasons