import pandas as pd

def preprocess(df):

    df.drop_duplicates(inplace=True)
    df = df.rename(columns={'personName': 'Billionaires', 'finalWorth': 'NetWorth(Million$)', 'source': 'company'})

    return df