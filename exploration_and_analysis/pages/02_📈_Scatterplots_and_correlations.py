"""
Page for dasboard displaying the scatterplots and correlations.
"""

import streamlit as st
from project_code.data_cleaning import load_indicator_data
from project_code.visualization import (
    correlation_scatterplot,
    animated_scatter,
    scatterplot_3d,
)
from project_code.analysis import calculate_correlations, partial_corr

st.set_page_config(page_title="The Wealth of Nations", layout="wide", page_icon="🗺️")

st.title("📈 Scatterplots and Correlations")
st.markdown("""
## Explore correlation between two indicators per chosen year or see the animated version over the years.
""")

# Load data
data = load_indicator_data(rename_countries=True)

# Let user select indicators
indicators = list(data.keys())
indicator_display_names = {
    name: name.replace("_", " ").title() for name in indicators
}
default_indicator_x = indicators.index("life_expectancy")

indicator_x = st.selectbox(
    "Select X indicator",
    options=indicators,
    format_func=lambda x: indicator_display_names[x],
    key="x_indicator_selectbox",
    index=default_indicator_x
)

# Remove the selected X indicator from Y options
available_for_y = [ind for ind in indicators if ind != indicator_x]
default_indicator_y = indicators.index("co2_per_capita")

indicator_y = st.selectbox(
    "Select Y indicator",
    options=available_for_y,
    format_func=lambda x: indicator_display_names[x],
    key="y_indicator_selectbox",
    index=default_indicator_y
) 

# Let user choose a year
year = st.slider(
    "Select year",
    min_value=min(data[indicator_x]["year"]),
    max_value=max(data[indicator_x]["year"]),
    value=max(data[indicator_x]["year"]),  # default latest year
)

st.markdown(" Click on the button below to view the animated version.")
if st.button(" ▶  Animate over years", key="animate_button"):
    fig1_anim = animated_scatter(data, indicator_x, indicator_y)
    st.plotly_chart(fig1_anim)

# Generate scatterplot
fig1 = correlation_scatterplot(data, indicator_x, indicator_y, year)
st.plotly_chart(fig1)

correlation = calculate_correlations(data, indicator_x, indicator_y, year)
# Show correlation for selected year
st.markdown(
    f"> Correlation coefficient: {correlation:.2f}"
)  # rounded to 2 decimal places

st.markdown(
    """
Did you find any shocking correlations? I know, seeing that there is negative correlation 
between pollution and mortality might seem counter-intuitive at first. But remember, correlation 
does not imply causation! This is why we cannot relay on only correlation bewteen two variables 
to draw conclusions about their relationship. Let's look at a 3D scatterplot including GDP per 
capita as a third variable to see if that helps explain the relationship better. GDP per capita 
helps to account for differences in wealth between countries, which can impactall of the indicators.
"""
)

# Scatterplot 3D with GDP per capita as third variable
indicator_z = "gdp_per_capita"

fig2 = scatterplot_3d(data, indicator_x, indicator_y, indicator_z, year)
st.plotly_chart(fig2)

partial_correlation = partial_corr(data, indicator_x, indicator_y, indicator_z, year)
# Show partial correlation for selected year
st.markdown(
    f"> Partial correlation coefficient for the selected indicators controlling for GDP: "
    f"{partial_correlation:.2f}"
)
