import pandas as pd

def load_data():
    df = pd.read_csv("data/globalterrorism.csv", encoding="latin1", low_memory=False)
    return df