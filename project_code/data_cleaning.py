import wbgapi as wb
import pandas as pd
import numpy as np

df = pd.read_csv("/Users/jarka/Desktop/Python-project/data/raw/all_indicators.csv")

# Select only the numeric columns (years)
year_cols = df.columns[2:]

# Sort indicators by missing fraction in descending order
missing_per_indicator = df.groupby('series')[year_cols].apply(lambda x: x.isna().mean().mean())
print("Missing values per indicator:")
print(missing_per_indicator.sort_values(ascending=False))

# Drop least covered ones from the DataFrame
df_clean1 = df[~df['series'].isin(['SH.STA.WASH.P5', 'SH.STA.AIRP.P5', 'SH.H2O.SMDW.ZS'])]

year_cols = df_clean1.columns[2:]

# Calculate missing fraction per country
missing_per_country = df_clean1.groupby('economy')[year_cols].apply(lambda x: x.isna().mean().mean())
print("Missing values per country:")
print(missing_per_country.sort_values(ascending=False))


