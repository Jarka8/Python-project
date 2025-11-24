import streamlit as st
import plotly.express as px
import sys
import os

# Add project root to Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from visualization import correlation_scatterplot
from data_cleaning import load_indicator_data

# Load data
data = load_indicator_data()

# Select indicators
x_ind = st.sidebar.selectbox("Indicator X", list(data.keys()))
y_ind = st.sidebar.selectbox("Indicator Y", list(data.keys()))

# Scatterplot function call
figures = correlation_scatterplot(data, x_ind, y_ind)

# Select year to show
year = st.sidebar.selectbox("Select Year", sorted(figures.keys()))

# Display
st.plotly_chart(figures[year])