import streamlit as st
import sys
from pathlib import Path
# Add project root to Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))
from project_code.data_cleaning import load_indicator_data    
from project_code.visualization import correlation_scatterplot

# Streamlit app 
st.title("The Wealth of Nations: Analysing Economic Environmental and Health Indicators")

# Load data
data = load_indicator_data()

# Let user select indicators
indicators = list(data.keys())

indicator_display_names = {
    name: name.replace("_", " ").title() 
    for name in indicators
}

indicator_x = st.selectbox("Select X indicator", options=indicators, format_func=lambda x: indicator_display_names[x])

# Remove the selected X indicator from Y options
available_for_y = [ind for ind in data.keys() if ind != indicator_x]
indicator_y = st.selectbox("Select Y indicator", options=available_for_y, format_func=lambda x: indicator_display_names[x])


# Generate scatterplots for all years
figs = correlation_scatterplot(data, indicator_x, indicator_y)

# Let user choose a year
year = st.slider("Select year", min_value=min(figs.keys()), max_value=max(figs.keys()), value=min(figs.keys()))
st.plotly_chart(figs[year])