import wbgapi as wb
import pandas as pd
print(wb.source.info())


WDI = 2  # second database = WDI (World Development Indicators)

economies = pd.DataFrame(wb.economy.list())

print(f"\nTotal economies: {len(economies)}")
print(f"\nColumns available: {list(economies.columns)}")


print("\n>>>>>>> ENVIRONMENT RELATED INDICATORS >>>>>>>>")
for term in ['!CO2', 'pollution', 'renewable energy', 'forest', 'deforestation', 'water']:
    for ind in wb.series.list(db=WDI, q=term):
        print(f"{ind['id']}: {ind['value']}")

print(">>>>>>> AID RELATED INDICATORS >>>>>>>>")
for term in ['official development assistance', 'ODA', 'aid']:
    for ind in wb.series.list(db=WDI, q=term):
        print(f"{ind['id']}: {ind['value']}")


print("\nFirst 20 economies:")
print(economies[['id', 'value', 'region', 'incomeLevel']].head(20))

all_indicators = list(wb.series.list(db=WDI))

print(f"\nTotal indicators in WDI: {len(all_indicators)}")
    
data_sample = wb.data.DataFrame(
    'NY.GDP.MKTP.KD.ZG',  # GDP growth (annual %)
    time=range(2015, 2023)
)

print(data_sample.head())
print(data_sample.shape)   