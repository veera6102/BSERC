import pandas as pd

def prepare_ml_data(df):
    """
    Filters, cleans, and structures the primary Global Terrorism Database (GTD)
    to feed uniform feature spaces into Machine Learning training pipelines.
    """
    # 1. Define the mandatory analytical feature dimensions and target column
    columns = [
        "country_txt",
        "region_txt",
        "targtype1_txt",
        "weaptype1_txt",
        "iyear",
        "success",
        "suicide",
        "attacktype1_txt"  # The target variable we want to predict
    ]
    
    # 2. Extract column dimensions safely using a deep copy to avoid slicing errors
    ml_df = df[columns].copy()
    
    # 3. Purge missing records to guarantee categorical vector mapping consistency
    ml_df = ml_df.dropna()
    
    return ml_df