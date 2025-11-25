import streamlit as st
import sys
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(project_root))
from project_code.data_cleaning import load_indicator_data
from project_code.visualization import correlation_scatterplot, calculate_correlations, scatterplot_3d

# Streamlit app
st.title(
    "The Wealth of Nations: Analysing Economic Environmental and Health Indicators"
)
st.write("Scatterplots to explore correlation between two indicators per chosen year.")
st.markdown("Choose indicators for the X and Y axes and see how they relate.")

# Load data
data = load_indicator_data(rename_countries=True)

# Let user select indicators
indicators = list(data.keys())

indicator_display_names = {name: name.replace("_", " ").title() for name in indicators}

indicator_x = st.selectbox(
    "Select X indicator",
    options=indicators,
    format_func=lambda x: indicator_display_names[x],
    key="x_indicator_selectbox"
)

# Remove the selected X indicator from Y options
available_for_y = [ind for ind in data.keys() if ind != indicator_x]
indicator_y = st.selectbox(
    "Select Y indicator",
    options=available_for_y,
    format_func=lambda x: indicator_display_names[x],
    key="y_indicator_selectbox"
)

# Generate scatterplots for all years
figs = correlation_scatterplot(data, indicator_x, indicator_y)

# Let user choose a year
year = st.slider(
    "Select year",
    min_value=min(figs.keys()),
    max_value=max(figs.keys()),
    value=max(figs.keys()), # default latest year
    key="scatter_year_slider"
)
st.plotly_chart(figs[year])

corr_values = calculate_correlations(data, indicator_x, indicator_y)
# Show correlation for selected year
st.write(f"Correlation coefficient: {corr_values[year]:.2f}") # round to 2 decimal places

st.markdown("""Did you find any shocking correlations? I know, seeing that there is negative correlation between
pollution and mortality might seem counter-intuitive at first. But remember, correlation does not imply causation!
This is why we cannot relay on only correlation bewteen two variables to draw conclusions about their relationship.
Let's look at a 3D scatterplot including GDP per capita as a third variable to see if that helps explain the 
relationship better. GDP per capita helps to account for differences in wealth between countries, which can impact
all of the indicators.""")


default_indicator_a = indicators.index("life_expectancy")
indicator_a = st.selectbox(
    "Select X indicator",
    options=indicators,
    format_func=lambda x: indicator_display_names[x],
    index=default_indicator_a,
    key="3d_x_indicator_selectbox"
)
default_indicator_b = indicators.index("co2_per_capita")
available_for_b = [ind for ind in data.keys() if ind != indicator_a]
indicator_b = st.selectbox(
    "Select Y indicator",
    options=available_for_b,
    format_func=lambda x: indicator_display_names[x],
    index=default_indicator_b,
    key="3d_y_indicator_selectbox"
)
indicator_c = "gdp_per_capita"

all_years = sorted(data[indicator_c]["year"].unique())
year2 = st.slider(
    "Select year", 
    min_value=min(all_years), 
    max_value=max(all_years), 
    value=max(all_years),
    key="3d_year_slider"
)

fig = scatterplot_3d(data, indicator_a, indicator_b, indicator_c, year2)
st.plotly_chart(fig)
