import plotly.express as px
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import statsmodels.api as sm
import numpy as np
import pandas as pd
import plotly.express as px
import streamlit as st

def map_plot(data, indicator, year):
    """
    Creates a choropleth map for a given indicator and year.
    """
    # Get the data for the selected indicator
    df = data[indicator]

    # Detect the value column (only non economy/year column)
    value_col = [col for col in df.columns if col not in ['economy', 'year']][0]

    # Filter for selected year
    df_year = df[df["year"] == year]

    # Create map
    map_plot = px.choropleth(
        df_year,
        locations="economy",     
        color=value_col, # makes color shade based on indicator values
        hover_name="economy",
        color_continuous_scale="Viridis", 
        projection="natural earth", 
        title=f"{indicator.replace('_',' ').title()} — {year}"
    )

    return map_plot


def scatterplot_3d(data: dict, x_indicator: str, y_indicator: str, z_indicator: str, year: int):
    """
    Creates a 3D scatterplot for a selected year from separate long-format DataFrames.
    
    Parameters:
    - data: dict of DataFrames keyed by indicator name
    - x_indicator, y_indicator, z_indicator: keys in `data` dict
    - year: int
    """
    # Merge the three indicators
    df_x = data[x_indicator]
    df_y = data[y_indicator]
    df_z = data[z_indicator]
    
    merged = df_x.merge(df_y, on=["economy", "year"]).merge(df_z, on=["economy", "year"])
    
    # Detect value columns
    val_x = [c for c in df_x.columns if c not in ["economy", "year"]][0]
    val_y = [c for c in df_y.columns if c not in ["economy", "year"]][0]
    val_z = [c for c in df_z.columns if c not in ["economy", "year"]][0]
    
    # Filter for selected year and drop missing
    temp = merged[merged["year"] == year]
    if temp.empty:
        st.warning(f"No data available for {year} with selected indicators.")
    
    # Create 3D scatterplot
    fig = px.scatter_3d(
        temp,
        x=val_x,
        y=val_y,
        z=val_z,
        hover_name='economy',
        color=val_z,
        labels={val_x: x_indicator.replace("_", " ").title(),
                val_y: y_indicator.replace("_", " ").title(),
                val_z: z_indicator.replace("_", " ").title()},
        title=f"{x_indicator.replace('_', ' ').title()} vs {y_indicator.replace('_', ' ').title()} vs {z_indicator.replace('_', ' ').title()} ({year})"
    )
    fig.update_layout(margin=dict(l=0, r=0, b=0, t=50))
    
    return fig

def correlation_scatterplot(data, indicator_x, indicator_y):
    """
    Creates year-by-year scatterplots for two indicators across all years.
    """
    # Get data for the two indicators
    df_x = data[indicator_x]
    df_y = data[indicator_y]
    
    # Detect value columns (only column that's not economy or year)
    val_x = [col for col in df_x.columns if col not in ["economy", "year"]][0]
    val_y = [col for col in df_y.columns if col not in ["economy", "year"]][0]

    # Merge on economy + year (inner join to keep only matching entries)
    merged = df_x.merge(df_y, on=["economy", "year"], how="inner") 
    # Remove missing values
    merged = merged.dropna(subset=[val_x, val_y])

    # Create scatterplots for each year
    years = sorted(merged["year"].unique())
    figs = {}  # store figures by year
    for yr in years:
        # Create a temporary DataFrame for the year
        temp = merged[merged["year"] == yr]
        # Plot
        fig = px.scatter(
            temp, 
            x = val_x,
            y = val_y,
            hover_name = "economy", # show country names on hover
            trendline = "ols",  # ordinary least squares regression line
            trendline_color_override = "orange",
            title = f"{indicator_x.replace("_", " ").title()} vs {indicator_y.replace("_", " ").title()} ({yr})",
            labels = {
                val_x: indicator_x.replace("_", " ").title(),
                val_y: indicator_y.replace("_", " ").title()
                }
        )
        figs[yr] = fig

    return figs




def calculate_correlations(data, indicator_x, indicator_y):
    """
    Calculates correlation coefficients for two indicators across all years.
    """
    # Get data for the two indicators
    df_x = data[indicator_x].copy()
    df_y = data[indicator_y].copy()
    
    # Detect value columns
    val_x = [col for col in df_x.columns if col not in ["economy", "year"]][0]
    val_y = [col for col in df_y.columns if col not in ["economy", "year"]][0]
    
    # Rename to avoid conflicts
    df_x = df_x.rename(columns={val_x: "value_x"})
    df_y = df_y.rename(columns={val_y: "value_y"})
    
    # Merge and clean
    merged = df_x.merge(df_y, on=["economy", "year"], how="inner")
    merged = merged.dropna(subset=["value_x", "value_y"])
    
    # Calculate correlations for each year
    years = sorted(merged["year"].unique())
    corr_values = {}
    
    for yr in years:
        temp = merged[merged["year"] == yr]
        corr_values[yr] = np.corrcoef(temp["value_x"], temp["value_y"])[0, 1] # correlation of x and y
    
    return corr_values


def animated_scatter(data, indicator_x, indicator_y):
    """
    Creates an animated scatterplot using two separate long-format indicator CSVs.
    """
    # Get data for the two indicators
    df_x = data[indicator_x]
    df_y = data[indicator_y]

    # Icdentify value columns
    val_x = [c for c in df_x.columns if c not in ["economy", "year"]][0]
    val_y = [c for c in df_y.columns if c not in ["economy", "year"]][0]

    # Merge
    merged = df_x.merge(df_y, on=["economy", "year"])
    merged = merged.dropna(subset=[val_x, val_y])

    years = sorted(merged["year"].unique())

    # Setup figure
    fig, ax = plt.subplots(figsize=(7, 6))

    def update(year):
        ax.clear()
        temp = merged[merged["year"] == year]
        ax.scatter(temp[val_x], temp[val_y])
        ax.set_title(f"{val_x} vs {val_y} — {year}")
        ax.set_xlabel(val_x.replace("_", " ").title())
        ax.set_ylabel(val_y.replace("_", " ").title())
        ax.grid(alpha=0.3)

    anim = FuncAnimation(fig, update, frames=years, interval=700)
    plt.show()


