import pandas as pd
import numpy as np


def compute_data_driven_weights(df):
    """
    Dynamically computes weights for weapons and targets based on historical GTD data.
    Normalizes the average casualties (kills + wounds) to a 10-40 scale.
    """
    if "nkill" in df.columns and "nwound" in df.columns:
        total_cas = df["nkill"].fillna(0) + df["nwound"].fillna(0)
    else:
        total_cas = pd.Series(0, index=df.index)

    temp = df.assign(_total_casualties=total_cas)

    weapon_stats = temp.groupby("weaptype1_txt")["_total_casualties"].mean().to_dict()
    max_weap_avg = max(weapon_stats.values()) if weapon_stats and max(weapon_stats.values()) > 0 else 1
    weapon_scores = {k: int(10 + (v / max_weap_avg) * 30) for k, v in weapon_stats.items()}

    target_stats = temp.groupby("targtype1_txt")["_total_casualties"].mean().to_dict()
    max_targ_avg = max(target_stats.values()) if target_stats and max(target_stats.values()) > 0 else 1
    target_scores = {k: int(10 + (v / max_targ_avg) * 30) for k, v in target_stats.items()}

    return weapon_scores, target_scores


def calculate_risk(weapon, target, success, suicide, casualties, df=None, return_breakdown=False):
    """
    Calculates a transparent risk score (0-120) and corresponding threat level.
    Uses data-driven scoring if a DataFrame is provided, otherwise falls back to standard baselines.
    """
    score = 0
    reasons = []

    DEFAULT_WEAPON_SCORE = {
        "Biological": 40,
        "Chemical": 35,
        "Explosives": 30,
        "Firearms": 25,
        "Incendiary": 20,
        "Melee": 10,
    }
    DEFAULT_TARGET_SCORE = {
        "Military": 30,
        "Police": 25,
        "Government (General)": 20,
        "Private Citizens & Property": 15,
        "Business": 10,
    }

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

    # 1. Weapon Score Impact (max 40)
    score += weapon_weight
    reasons.append(f"Weapon Impact ({weapon}) [{basis_type}]: +{weapon_weight} pts")

    # 2. Target Score Impact (max 40)
    score += target_weight
    reasons.append(f"Target Vulnerability ({target}) [{basis_type}]: +{target_weight} pts")

    # 3. Success Status Impact (max 10)
    success_pts = 10 if success == 1 else 0
    score += success_pts
    if success_pts > 0:
        reasons.append("Successful Incident Mechanics: +10 pts")
    else:
        reasons.append("Contained / Failed Execution Status: +0 pts")

    # 4. Tactical Intent - Suicide Attack (max 15)
    suicide_pts = 15 if suicide == 1 else 0
    score += suicide_pts
    if suicide_pts > 0:
        reasons.append("High-Intensity Tactical Profile (Suicide Attack): +15 pts")
    else:
        reasons.append("Standard Non-Suicide Operational Mode: +0 pts")

    # 5. Severity Metrics - Casualties Impact (max 30)
    if casualties >= 50:
        cas_pts = 30
        reasons.append("Mass-Casualty Threshold Met (>= 50): +30 pts")
    elif casualties >= 20:
        cas_pts = 20
        reasons.append("Elevated Casualty Scale Met (>= 20): +20 pts")
    elif casualties >= 10:
        cas_pts = 10
        reasons.append("Moderate Casualty Scale Met (>= 10): +10 pts")
    elif casualties > 0:
        cas_pts = 5
        reasons.append("Minor Casualty Scale Impact (> 0): +5 pts")
    else:
        cas_pts = 0
        reasons.append("Zero Confirmed Casualties Logged: +0 pts")

    score += cas_pts
    score = min(int(score), 120)

    # 6. Determine Final Normalized Threat Level Classification
    if score < 35:
        level = "LOW"
    elif score < 65:
        level = "MODERATE"
    elif score < 85:
        level = "HIGH"
    else:
        level = "CRITICAL"

    if return_breakdown:
        breakdown = {
            "Weapon Lethality": weapon_weight,
            "Target Vulnerability": target_weight,
            "Execution Success": success_pts,
            "Suicide Modality": suicide_pts,
            "Casualty Severity": cas_pts,
        }
        return score, level, reasons, breakdown

    return score, level, reasons


def get_posture_recommendations(level: str) -> list[str]:
    """Returns defensive analytical recommendations matched to the classified threat level."""
    postures = {
        "LOW": [
            "Maintain baseline perimeter monitoring and routine historical logging.",
            "Conduct standard periodic vulnerability reviews on target sector assets.",
            "Continue passive intelligence collection with normal reporting cadence.",
        ],
        "MODERATE": [
            "Increase situational awareness and cross-check regional incident clusters.",
            "Review physical access controls and blast/ballistic standoff perimeters.",
            "Coordinate inter-agency information sharing on repeat weapon modalities.",
        ],
        "HIGH": [
            "Harden high-value target sectors and enforce strict vehicle/package screening.",
            "Establish rapid-response medical and EOD readiness protocols in hotspot zones.",
            "Perform deep-dive attribution cross-checks against known regional perpetrator groups.",
        ],
        "CRITICAL": [
            "Activate maximum defensive posture and mass-casualty contingency frameworks.",
            "Deploy multi-layered counter-IED / counter-assault protective rings around critical infrastructure.",
            "Initiate continuous executive threat monitoring and emergency response coordination.",
        ],
    }
    return postures.get(level, postures["MODERATE"])
