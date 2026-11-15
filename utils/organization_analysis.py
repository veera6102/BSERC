import pandas as pd


def top_organizations(df, n=50):
    """
    Isolates and returns the top N highest-volume perpetrator organizations
    ranked by historical incident frequency, excluding 'Unknown'.
    """
    org_col = "gname" if "gname" in df.columns else "gname_txt"
    filtered = df[df[org_col].notna() & (df[org_col] != "Unknown")]
    return filtered[org_col].value_counts().head(n).index.tolist()


def organization_summary_kpis(df, selected_org):
    """Computes key operational metrics for a selected perpetrator organization."""
    org_col = "gname" if "gname" in df.columns else "gname_txt"
    org_data = df[df[org_col] == selected_org]
    if org_data.empty:
        return {
            "incidents": 0,
            "kills": 0,
            "wounds": 0,
            "casualties": 0,
            "success_rate": 0.0,
            "primary_country": "N/A",
            "active_span": "N/A",
        }

    incidents = len(org_data)
    kills = int(org_data["nkill"].fillna(0).sum()) if "nkill" in org_data.columns else 0
    wounds = int(org_data["nwound"].fillna(0).sum()) if "nwound" in org_data.columns else 0
    success_rate = (
        float(org_data["success"].fillna(0).mean() * 100)
        if "success" in org_data.columns
        else 0.0
    )
    primary_country = (
        str(org_data["country_txt"].mode().iloc[0])
        if "country_txt" in org_data.columns and not org_data["country_txt"].dropna().empty
        else "N/A"
    )
    if "iyear" in org_data.columns and not org_data["iyear"].dropna().empty:
        min_y, max_y = int(org_data["iyear"].min()), int(org_data["iyear"].max())
        active_span = f"{min_y}–{max_y}" if min_y != max_y else f"{min_y}"
    else:
        active_span = "N/A"

    return {
        "incidents": incidents,
        "kills": kills,
        "wounds": wounds,
        "casualties": kills + wounds,
        "success_rate": success_rate,
        "primary_country": primary_country,
        "active_span": active_span,
    }


def organization_yearly(df, selected_org):
    """Aggregates yearly chronological frequency distributions for line graphs."""
    org_col = "gname" if "gname" in df.columns else "gname_txt"
    org_data = df[df[org_col] == selected_org].copy()
    if org_data.empty:
        return pd.DataFrame(columns=["Year", "Count"])

    timeline = org_data.groupby("iyear").size().reset_index(name="Count")
    timeline.columns = ["Year", "Count"]
    return timeline


def organization_attack_types(df, selected_org):
    """Computes preferred historical vector metrics for attack profiles."""
    org_col = "gname" if "gname" in df.columns else "gname_txt"
    atk_col = "attacktype1_txt" if "attacktype1_txt" in df.columns else "attacktype1"
    org_data = df[df[org_col] == selected_org].copy()
    if org_data.empty:
        return pd.DataFrame(columns=["Attack Type", "Count"])

    attacks = org_data.groupby(atk_col).size().reset_index(name="Count")
    attacks.columns = ["Attack Type", "Count"]
    return attacks.sort_values(by="Count", ascending=False)


def organization_weapons(df, selected_org):
    """Tracks tactical weapon system framework distributions."""
    org_col = "gname" if "gname" in df.columns else "gname_txt"
    weap_col = "weaptype1_txt" if "weaptype1_txt" in df.columns else "weaptype1"
    org_data = df[df[org_col] == selected_org].copy()
    if org_data.empty:
        return pd.DataFrame(columns=["Weapon", "Count"])

    weapons = org_data.groupby(weap_col).size().reset_index(name="Count")
    weapons.columns = ["Weapon", "Count"]
    return weapons.sort_values(by="Count", ascending=False)


def organization_targets(df, selected_org):
    """Tracks targeted victim/infrastructure sectors for the selected organization."""
    org_col = "gname" if "gname" in df.columns else "gname_txt"
    targ_col = "targtype1_txt" if "targtype1_txt" in df.columns else "targtype1"
    org_data = df[df[org_col] == selected_org].copy()
    if org_data.empty:
        return pd.DataFrame(columns=["Target Sector", "Count"])

    targets = org_data.groupby(targ_col).size().reset_index(name="Count")
    targets.columns = ["Target Sector", "Count"]
    return targets.sort_values(by="Count", ascending=False)
