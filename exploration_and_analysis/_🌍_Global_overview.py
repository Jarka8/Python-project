"""
The main page of the interactive dasboard.
"""

import os
import streamlit as st
import sys
from pathlib import Path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))
from project_code.main import setup
from project_code.data_cleaning import load_indicator_data
from project_code.visualization import plot_map

if not os.path.exists("data/long"):
    with st.spinner("Setting up data for the first time... This may take a minute."):
        setup()
    st.success("Data setup complete!")

st.set_page_config(
    page_title="The Wealth of Nations",
    layout="wide",
    page_icon="🗺️"
)

# Streamlit app
st.title("🗺️ The Wealth of Nations")

st.markdown("## Analysing Economic Environmental and Health Indicators")

st.markdown("""
This dashboard allows you to explore various economic, environmental, and health 
indicators for countries around the world. On this page you can select one indicator
and a year to see its values per country on the map. Just hover over countries and explore.
To compare two indicators and see how they correlate with each other, go to the Scatterplots 
page. Does the health and environment of a nation improve with its wealth? Find out!
""")

st.markdown("""
Some countries with higher GDP also show better health indicators — but what about their pollution levels? 
Could industrial growth be affecting air quality and, in turn, health or does the health expenditure offset this? 
How might these relationships evolve over time? Explore the charts to uncover possible connections between 
the economy, environment, and well-being.
""")

# Load data
data = load_indicator_data(rename_countries=False)

# Let user select indicator
indicators = list(data.keys())
default_indicator = "life_expectancy"
indicator_display_names = {name: name.replace("_", " ").title() for name in indicators}
indicator = st.selectbox(
    "Select indicator", 
    options=indicators, 
    format_func=lambda x: indicator_display_names[x],
    index=indicators.index(default_indicator)
    )

# Drop NAs so the years with no data are not available
for ind in data:
    data[ind] = data[ind].dropna()

# and year
year = st.slider(
    "Select year",
    min_value=min(data[indicator]["year"]),
    max_value=max(data[indicator]["year"]),
    value=max(data[indicator]["year"])  
)

plot_chor_map = plot_map(data, indicator, year)
st.plotly_chart(plot_chor_map)
