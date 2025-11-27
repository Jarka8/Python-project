"""
The page for the dashboard which explains each available indicator.
"""

import streamlit as st

st.set_page_config(
    page_title="The Wealth of Nations",
    layout="wide",
    page_icon="🗺️"
)

st.title("📖 Indicator Guide")

st.markdown("""
## 🔎 A Guide to the available indicators

To help you explore global development patterns, the dashboard includes key indicators across the economy, health, environment, and population.  
Below is a short description of what each variable represents and why it matters.

---

## 💸 Economy
- **GDP per capita, PPP (constant 2021 international $)**  
  Measures average economic output per person, allowing comparisons across countries by adjusting for price levels.

- **GDP growth (annual %)**  
  Shows how quickly an economy is expanding or contracting.

- **Carbon intensity of GDP (kg CO₂e per 2021 PPP $ of GDP)**  
  Indicates how much CO₂ is emitted per unit of economic activity — a key indicator of sustainable growth.

---

## 🩺 Health
- **Life expectancy at birth (years)**  
  A broad measure of population health and quality of life.

- **Under-5 mortality rate (per 1,000 live births)**  
  Reflects healthcare access, maternal health, and child nutrition.

- **Current health expenditure (% of GDP)**  
  Shows the share of national resources invested into health.

- **Health expenditure per capita (current US$)**  
  Average healthcare spending per person — useful for comparing health system financing.

---

## 🌍 Environment
- **CO₂ emissions per capita (t CO₂e/person)**  
  Measures each individual’s contribution to emissions — reflects lifestyle, energy mix, and economic structure.

- **PM2.5 pollution (µg/m³)**  
  Average annual exposure to fine particulate matter; high values indicate poor air quality.

- **Total greenhouse gas emissions per capita (t CO₂e/person)**  
  Broader than CO₂, includes methane, nitrous oxide, etc.

- **Renewable energy consumption (% of total)**  
  Shows progress toward clean energy transitions.

- **Forest area (% of land area)**  
  Indicates biodiversity health, carbon absorption, and resilience to climate change.

---

## 👩🏼‍🤝‍👩🏿 Population & Urbanization
- **Population growth (annual %)**  
  Shows how fast the population is increasing or decreasing.

- **Total population**  
  Basic demographic size, useful for scaling other indicators.

- **Urban population (% of total)**  
  Measures share of people living in cities — linked to infrastructure needs, emissions, and economic structure.

---
""")
