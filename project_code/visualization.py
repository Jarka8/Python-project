"""
This module contains functions for the visualisation of the indicators
such as choropleth map, scatterplot, 3D scatterplot
"""

import plotly.express as px
import streamlit as st
from project_code.utils import merge_indicators
import pandas as pd


def plot_map(data, indicator, year):
    """
    Creates a choropleth map for a given indicator and year.
    """
    # Get the data for the selected indicator
    df = data[indicator]

    # Detect the value column (only non economy/year column)
    value_col = [col for col in df.columns if col not in ["economy", "year"]][0]

    # Filter for selected year
    df_year = df[df["year"] == year]

    # Create map
    plot_map = px.choropleth(
        df_year,
        locations="economy",
        color=value_col,  # makes color shade based on indicator values
        hover_name="economy",
        color_continuous_scale="RdYlGn_r",
        projection="natural earth",
        title=f"{indicator.replace('_',' ').title()} — {year}",
    )
    plot_map.update_layout(margin={"r": 0, "t": 50, "l": 0, "b": 0})
    return plot_map


def correlation_scatterplot(data, ind_x, ind_y, year):
    """
    Creates year-by-year scatterplots for two indicators across all years.
    """
    # Merge the two indicators
    df, val_cols = merge_indicators(data, [ind_x, ind_y])

    # Detect value columns
    val_x = val_cols[ind_x]
    val_y = val_cols[ind_y]

    # Create a temporary DataFrame for the year
    df = df[df["year"] == year]

    # Plot
    fig = px.scatter(
        df,
        x=val_x,
        y=val_y,
        hover_name="economy",  # show country names on hover
        trendline="ols",  # ordinary least squares regression line
        trendline_color_override="orange",
        title=f"{ind_x.replace("_", " ").title()} vs {ind_y.replace("_", " ").title()} ({year})",
        labels={
            val_x: ind_x.replace("_", " ").title(),
            val_y: ind_y.replace("_", " ").title(),
        },
    )

    return fig


def scatterplot_3d(data, ind_x, ind_y, ind_z, year):
    """
    Creates a 3D scatterplot for a selected year from separate long-format DataFrames.

    Parameters:
    - data: dict of DataFrames keyed by indicator name
    - x_indicator, y_indicator, z_indicator: keys in `data` dict
    - year: int
    """
    # Merge the three indicators
    df, val_cols = merge_indicators(data, [ind_x, ind_y, ind_z])

    # Detect value columns
    val_x = val_cols[ind_x]
    val_y = val_cols[ind_y]
    val_z = val_cols[ind_z]

    # Filter for selected year
    temp = df[df["year"] == year]
    if temp.empty:
        st.warning(f"No data available for {year} with selected indicators.")

    # Create 3D scatterplot
    fig = px.scatter_3d(
        temp,
        x=val_x,
        y=val_y,
        z=val_z,
        height=600,
        hover_name="economy",
        color=val_z,
        labels={
            val_x: ind_x.replace("_", " ").title(),
            val_y: ind_y.replace("_", " ").title(),
            val_z: ind_z.replace("_", " ").title(),
        },
        title=(
            f"{ind_x.replace('_', ' ').title()} vs {ind_y.replace('_', ' ').title()}"
            f"vs {ind_z.replace('_', ' ').title()} ({year})"
        ),
    )
    return fig


def animated_scatter(data, ind_x, ind_y):
    """
    Creates an animated scatterplot using two indicators across years.
    """
    # Merge the two indicators
    df, val_cols = merge_indicators(data, [ind_x, ind_y])

    # Detect value columns
    val_x = val_cols[ind_x]
    val_y = val_cols[ind_y]

    # Create animated scatterplot
    fig = px.scatter(
        df,
        x=val_x,
        y=val_y,
        animation_frame="year",
        hover_name="economy",
        trendline="ols",  # ordinary least squares regression line
        trendline_color_override="orange",
        labels={
            val_x: ind_x.replace("_", " ").title(),
            val_y: ind_y.replace("_", " ").title(),
        },
        title=f"{ind_x.replace('_',' ').title()} vs {ind_y.replace('_',' ').title()} (animated)",
    )
    fig.update_layout(margin=dict(l=0, r=0, t=50, b=0))

    return fig


def regression_summary_table(result):
    """
    Returns a cleaned DataFrame with only main coefficients (exclude country dummies),
    rounded for easier reading and highlights significance.
    """
    df = ~result.params.index.str.startswith("C(economy)")

    summary_df = pd.DataFrame(
        {
            "Variables": [
                name.replace("_", " ").title() for name in result.params.index[df]
            ],
            "Coefficients": result.params[df].values,
            "Std. Error": result.bse[df].values,
            "t-value": result.tvalues[df].values,
            "P-value": result.pvalues[df].values,
            "CI 2.5%": result.conf_int()[df][0].values,
            "CI 97.5%": result.conf_int()[df][1].values,
        }
    )

    # Round numbers
    summary_df = summary_df.round(
        {
            "Coefficients": 3,
            "Std. Error": 3,
            "t-value": 3,
            "P-value": 3,
            "CI 2.5%": 3,
            "CI 97.5%": 3,
        }
    )

    return summary_df


def highlight_significant(row):
    """Highlights rows where p-value < 0.05"""
    if row["P-value"] < 0.05 and row["Variables"] != "Intercept":
        return ["background-color: lightgreen"] * len(row)
    else:
        return [""] * len(row)
