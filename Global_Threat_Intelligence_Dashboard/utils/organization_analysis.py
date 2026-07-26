import pandas as pd

def top_organizations(df, n=50):
    """
    Isolates and filters the highest volume perpetrator organizations
    excluding unknown or blank data placeholders.
    """
    org_col = "gname" if "gname" in df.columns else "gname_txt"
    filtered = df[df[org_col].notna() & (df[org_col] != "Unknown")]
    return sorted(filtered[org_col].unique().tolist())[:n]

def organization_yearly(df, selected_org):
    """
    Aggregates yearly chronological frequency distributions for line graphs.
    """
    org_col = "gname" if "gname" in df.columns else "gname_txt"
    org_data = df[df[org_col] == selected_org].copy()
    if org_data.empty:
        return pd.DataFrame(columns=['Year', 'Count'])
        
    timeline = org_data.groupby('iyear').size().reset_index(name='Count')
    timeline.columns = ['Year', 'Count']
    return timeline

def organization_attack_types(df, selected_org):
    """
    Computes preferred historical vector metrics for attack profiles.
    """
    org_col = "gname" if "gname" in df.columns else "gname_txt"
    atk_col = "attacktype1_txt" if "attacktype1_txt" in df.columns else "attacktype1"
    org_data = df[df[org_col] == selected_org].copy()
    if org_data.empty:
        return pd.DataFrame(columns=['Attack Type', 'Count'])
        
    attacks = org_data.groupby(atk_col).size().reset_index(name='Count')
    attacks.columns = ['Attack Type', 'Count']
    return attacks.sort_values(by='Count', ascending=False)

def organization_weapons(df, selected_org):
    """
    Tracks tactical weapon system framework distributions.
    """
    org_col = "gname" if "gname" in df.columns else "gname_txt"
    weap_col = "weaptype1_txt" if "weaptype1_txt" in df.columns else "weaptype1"
    org_data = df[df[org_col] == selected_org].copy()
    if org_data.empty:
        return pd.DataFrame(columns=['Weapon', 'Count'])
        
    weapons = org_data.groupby(weap_col).size().reset_index(name='Count')
    weapons.columns = ['Weapon', 'Count']
    return weapons.sort_values(by='Count', ascending=False)