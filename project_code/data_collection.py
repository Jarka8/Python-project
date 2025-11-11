import wbgapi as wb
import pandas as pd

# Getting list of non-aggregate economies
non_aggregates = [e for e in wb.economy.list() if not e['aggregate']]
economy_ids = [e['id'] for e in non_aggregates]

# Filtering economies with population > 5 million
min_pop = 5000000  # minimum population
pop_data = wb.data.DataFrame('SP.POP.TOTL', economy_ids)

# Selecting countries satisfying the population criterion for the last available year
filtered_countries = pop_data.index[pop_data.iloc[:, -1] >= min_pop].tolist()

indicators = [
    'EN.GHG.ALL.PC.CE.AR5', 'EN.GHG.CO2.PC.CE.AR5', 'EN.ATM.PM25.MC.M3', 'EN.GHG.CO2.RT.GDP.PP.KD',
    'NY.GDP.PCAP.PP.KD', 'NY.GDP.MKTP.KD.ZG', 'SP.DYN.LE00.IN', 'SH.DYN.MORT', 'SH.XPD.CHEX.GD.ZS', 
    'SH.XPD.CHEX.PC.CD', 'AG.LND.FRST.ZS', 'SH.H2O.SMDW.ZS', 'SH.STA.AIRP.P5', 'EG.FEC.RNEW.ZS', 
    'SH.STA.WASH.P5', 'SP.POP.GROW', 'SP.POP.TOTL', 'SP.URB.TOTL.IN.ZS'
]

data = wb.data.DataFrame(indicators, filtered_countries, time = range(2000, 2024))
data.to_csv("data/raw/all_indicators.csv")


exit()