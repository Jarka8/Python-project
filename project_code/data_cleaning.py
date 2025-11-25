import pandas as pd
import os
import glob
from pathlib import Path
import pycountry
import streamlit as st
import time

def clean_data():
    """Cleans the raw data - removing indicators and countries with significant missing data."""
    
    # Load raw data
    df = pd.read_csv("data/raw/all_indicators.csv")
    # Select only the numeric columns (years)
    year_cols = df.columns[2:]

    treshold = 0.3  # 30% missing data allowed

    # Sort indicators by missing fraction in descending order
    missing_per_indicator = df.groupby('series')[year_cols].apply(lambda x: x.isna().mean().mean())

    # Drop least covered ones 
    print(f"Indicators with over 30% of missing data {missing_per_indicator[missing_per_indicator > treshold]}")
    low_data_indicators = missing_per_indicator[missing_per_indicator > treshold].index
    df_clean1 = df[~df['series'].isin(low_data_indicators)]
    
    # Select only the numeric columns (years)
    year_cols = df_clean1.columns[2:]

    # Calculate missing fraction per country
    missing_per_country = df_clean1.groupby('economy')[year_cols].apply(lambda x: x.isna().mean().mean())
    
    # Drop countries with too much missing data
    print(f"Countries with over 30% of missing data {missing_per_country[missing_per_country > treshold]}")
    low_data_countries = missing_per_country[missing_per_country > treshold].index
    df_clean2 = df_clean1[~df_clean1['economy'].isin(low_data_countries)]
    
    path = "data/cleaned/all_indicators_cleaned.csv"
    df_clean2.to_csv(path, index=False)
    print(f"Cleaned data saved to {path}")

def split_data():
    """Splits the cleaned data into separate files per indicator."""
    
    # Load cleaned data
    df = pd.read_csv("data/cleaned/all_indicators_cleaned.csv")
    for indicator, subset in df.groupby("series"):
        # Clean year columns to contain only year number
        subset.columns = subset.columns.str.replace("YR", "")
        
        # Remove the indicator column (since file is per-indicator)
        subset = subset.drop(columns = ["series"])
    
        # Create readable filename
        indicator_names = {
            'AG.LND.FRST.ZS': 'forest_area',
            'EG.FEC.RNEW.ZS': 'renewable_energy',
            'EN.ATM.PM25.MC.M3': 'pm25_pollution',
            'EN.GHG.ALL.PC.CE.AR5': 'ghg_per_capita',
            'EN.GHG.CO2.PC.CE.AR5': 'co2_per_capita',
            'EN.GHG.CO2.RT.GDP.PP.KD': 'carbon_intensity',
            'NY.GDP.MKTP.KD.ZG': 'gdp_growth',
            'NY.GDP.PCAP.PP.KD': 'gdp_per_capita',
            'SH.DYN.MORT': 'child_mortality',
            'SH.XPD.CHEX.GD.ZS': 'health_exp_pct_gdp',
            'SH.XPD.CHEX.PC.CD': 'health_exp_per_capita',
            'SP.DYN.LE00.IN': 'life_expectancy',
            'SP.POP.GROW': 'population_growth',
            'SP.POP.TOTL': 'population',
            'SP.URB.TOTL.IN.ZS': 'urban_population'
        }
    
        filename = indicator_names.get(indicator)
        path = f"data/cleaned/{filename}.csv"
        subset.to_csv(path, index=False)
        print(f"Saved: {path}")


def long_format_data():
    """Converts each cleaned indicator file to long format and saves it."""
    # Get list of all CSV files in the cleaned folder
    csv_files = glob.glob("data/cleaned/*.csv")
    # Load each CSV, convert to long format, and save
    for f in csv_files:
        df = pd.read_csv(f)
        name = os.path.splitext(os.path.basename(f))[0]
        long_df = df.melt(id_vars=['economy'], var_name='year', value_name=name)
        os.makedirs("data/long", exist_ok=True)
        long_df.to_csv(f"data/long/{name}_long.csv", index=False)


def rename_economies(df):
    """Renames 3-letter country codes to full country names in the 'economy' column."""
    df = df.copy()
    # Create mapping dictionary
    code_to_country = {}
    for c in pycountry.countries:
        if hasattr(c, "alpha_3"):
            code_to_country[c.alpha_3] = c.name
    # Map codes to names
    df["economy"] = df["economy"].map(code_to_country).fillna(df["economy"])
    return df



@st.cache_data  # Streamlit will cache the result
def load_indicator_data(rename_countries=True):
    """
    Loads all long-format indicator CSVs from the cleaned data folder into a dictionary of DataFrames.
    rename_countries: If True, converts ISO codes to country names. If False, keeps ISO-3 codes.
    Returns: data (dict): Dictionary where keys are indicator names and values are DataFrames.
    """
    time.sleep(1)  # Simulate a delay for loading data
    project_root = Path(__file__).parent.parent
    data_path = project_root/"data"/"long"
    csv_files = glob.glob(str(data_path/"*.csv"))
    
    data = {}
    for f in csv_files:
        if os.path.basename(f) == "all_indicators_cleaned_long.csv":
            continue
        name = os.path.splitext(os.path.basename(f))[0]
        name = name.replace('_long', '')  
        df = pd.read_csv(f)
        # Rename countries only when needed 
        # (keeps codes for map but shows full names in scatterplots)
        if rename_countries:
            df = rename_economies(df)
        
        data[name] = df
        data[name] = df
    
    return data

