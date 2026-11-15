import os
import pandas as pd
import streamlit as st
from config import DATA_CSV_PATH, DATA_XLSX_PATH


@st.cache_data(show_spinner=False)
def load_data() -> pd.DataFrame:
    """
    Loads and caches the Global Terrorism Database (GTD) dataset.
    Automatically falls back to globalterrorism.xlsx if globalterrorism.csv
    is absent, and caches a CSV copy for fast subsequent reads.
    """
    if DATA_CSV_PATH.exists():
        try:
            df = pd.read_csv(DATA_CSV_PATH, encoding="utf-8", low_memory=False)
        except UnicodeDecodeError:
            df = pd.read_csv(DATA_CSV_PATH, encoding="latin1", low_memory=False)
    elif DATA_XLSX_PATH.exists():
        df = pd.read_excel(DATA_XLSX_PATH)
        try:
            df.to_csv(DATA_CSV_PATH, index=False, encoding="utf-8")
        except Exception:
            pass
    else:
        raise FileNotFoundError(
            f"Dataset not found at {DATA_CSV_PATH} or {DATA_XLSX_PATH}."
        )

    # Pre-compute standardized analytical columns safely
    if "nkill" in df.columns:
        df["nkill"] = pd.to_numeric(df["nkill"], errors="coerce").fillna(0)
    else:
        df["nkill"] = 0

    if "nwound" in df.columns:
        df["nwound"] = pd.to_numeric(df["nwound"], errors="coerce").fillna(0)
    else:
        df["nwound"] = 0

    df["total_casualties"] = df["nkill"] + df["nwound"]

    if "iyear" in df.columns:
        df["iyear"] = pd.to_numeric(df["iyear"], errors="coerce").fillna(1970).astype(int)

    return df
