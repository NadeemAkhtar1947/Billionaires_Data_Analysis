import numpy as np
import pandas as pd

def country_year_list(df):
    industry_list = np.unique(df['industries'].dropna().values).tolist()
    industry_list.sort()
    industry_list.insert(0, 'Overall')

    country_list = np.unique(df['country'].dropna().values).tolist()
    country_list.sort()
    country_list.insert(0, 'Overall')

    return  industry_list, country_list

def countrywise_billionaires(df,country):
    temp_df = df.dropna(subset=['Billionaires'])
    if country != 'Overall':
        temp_df = df[df['country'] == country]
    country_df = temp_df.groupby('country')['Billionaires'].count().reset_index().sort_values(by='Billionaires',ascending=False).head(60)

    return country_df

def industrywise_billionaires(df, industry):
    temp_df = df.dropna(subset=['industries'])
    if industry != 'Overall':
        temp_df = df[df['industries'] == industry]
    industry_df = temp_df.groupby('industries')['Billionaires'].count().reset_index().sort_values(by='Billionaires',ascending=False).head(60)

    return industry_df

def hello(df):
    data = pd.DataFrame({'age': np.random.normal(60, 10, 1000)})
    return data



def top_billionaires_by_country(df, country):
    df_billion = df[['NetWorth(Million$)', 'Billionaires', 'country', 'company']]
    x = None  # Initialize x as None
    if country == 'Overall':
        # Sort the entire DataFrame by wealth in descending order
        x = df_billion.sort_values(by='NetWorth(Million$)', ascending=False)
    else:
        country_df = df_billion[df_billion['country'] == country]
        country_df = country_df.sort_values(by='NetWorth(Million$)', ascending=False)
    top_ten_billionaires = x.head(20) if x is not None else country_df.head(20)

    return pd.DataFrame(top_ten_billionaires)
