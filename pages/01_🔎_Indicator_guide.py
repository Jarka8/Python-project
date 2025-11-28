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
  Measures average economic output per person, adjusted for cost of living differences across countries.  
  Core indicator of living standards and economic development.  
  
- **GDP growth (annual %)**  
  Shows how quickly an economy is expanding or contracting.  
  Reflects the rate of change in the total value of all goods and services produced.

- **Carbon intensity of GDP (kg CO₂e per 2021 PPP $ of GDP)**  
  Indicates how much CO₂ is emitted per unit of economic activity.  
  A key indicator of sustainable growth.

---

## 🩺 Health
- **Life expectancy at birth (years)**  
  Average number of years a newborn is expected to live.  
  A broad measure of population health, healthcare quality, and living conditions.

- **Child mortality rate (per 1,000 live births)**  
  Measures deaths of children under 5 per 1,000 births.  
  Reflects healthcare access, maternal health, and child nutrition.

- **Current health expenditure (% of GDP)**  
  Shows the share of national resources invested into health.  
  Indicates policy priorities and commitment to public health.

- **Health expenditure per capita (current US$)**  
  Average healthcare spending per person.  
  Resources available for healthcare services per individual, useful for comparing.

---

## 🌍 Environment
- **CO₂ emissions per capita (tonnes CO₂/person)**  
  Individual carbon footprint from fossil fuels and industry.  
  Key driver of climate change, reflects energy consumption.

- **PM2.5 pollution (µg/m³)**  
  Air pollution, particles < 2.5 micrometers.  
  Linked to respiratory disease, heart disease, and premature death.

- **Total greenhouse gas emissions per capita (tonnes/person)**  
  All greenhouse gases (CO₂, methane, nitrous oxide, etc.) per person.  
  More comprehensive than CO₂ alone, includes agriculture and waste, indicates air quality. 

- **Renewable energy consumption (% of total)**  
  Share of energy from renewable sources (solar, wind, hydro, etc.).  
  Shows progress toward clean energy transition.

- **Forest area (% of land area)**  
  Indicates biodiversity health, carbon absorption, and resilience to climate change.

---

## 👩🏼‍🤝‍👩🏿 Population & Urbanization
- **Population growth (annual %)**  
  Shows how fast the population is increasing or decreasing.  
  Affects resource needs, economic growth, and environmental pressure.

- **Total population**  
  Basic demographic size.  
  Baseline for calculating per capita indicators.

- **Urban population (% of total)**  
  Measures share of people living in cities.  
  Linked to infrastructure needs, emissions, and economic structure.

---
""")
