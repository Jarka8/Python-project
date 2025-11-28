"""
This module contains collec_data function which collects the data
for the indicators chosen after the analysis explained in the
project_analysis.ipynb from the World Bank API.
"""

import wbgapi as wb
import pandas as pd

def collect_data():
    """Collects raw data from the World Bank API and saves it to a CSV file."""

    # Getting list of non-aggregate economies
    non_aggregates = [e for e in wb.economy.list() if not e["aggregate"]]
    economy_ids = [e["id"] for e in non_aggregates]

    # Filtering economies with population > 5 million
    min_pop = 5000000  # minimum population
    pop_data = wb.data.DataFrame("SP.POP.TOTL", economy_ids)

    # Selecting countries satisfying the population criterion for the last available year
    filtered_countries = pop_data.index[pop_data.iloc[:, -1] >= min_pop].tolist()

    indicators = [
        "EN.GHG.ALL.PC.CE.AR5",
        "EN.GHG.CO2.PC.CE.AR5",
        "EN.ATM.PM25.MC.M3",
        "EN.GHG.CO2.RT.GDP.PP.KD",
        "NY.GDP.PCAP.PP.KD",
        "NY.GDP.MKTP.KD.ZG",
        "SP.DYN.LE00.IN",
        "SH.DYN.MORT",
        "SH.XPD.CHEX.GD.ZS",
        "SH.XPD.CHEX.PC.CD",
        "AG.LND.FRST.ZS",
        "SH.H2O.SMDW.ZS",
        "SH.STA.AIRP.P5",
        "EG.FEC.RNEW.ZS",
        "SH.STA.WASH.P5",
        "SP.POP.GROW",
        "SP.POP.TOTL",
        "SP.URB.TOTL.IN.ZS",
    ]

    print(
        "Collecting data from World Bank API this may take a while have a cup of coffee..."
    )
    data = wb.data.DataFrame(indicators, filtered_countries, time=range(2000, 2024))
    path = "data/raw/all_indicators.csv"
    data.to_csv(path)
    print(f"Raw data saved to {path}")


def ensure_valid_raw_data():
    """
    Ensures that the raw data file contains economy and series columns.
    If not, replaces it with the backup version.
    """
    csv_path = "data/raw/all_indicators.csv"
    backup_path = "data/raw/raw_data_backup.txt"
    df = pd.read_csv(csv_path)
    
    # Check the structure
    if "economy" in df.columns and "series" in df.columns:
        print("✔ Raw data structure is valid.")
        return
    else:
        print("⚠ Raw data missing required columns. Restoring backup...")
        backup_df = pd.read_csv(backup_path)
        # Save backup over wrong CSV
        backup_df.to_csv(csv_path, index=False)
        print("🔄 Raw data restored from backup.")
