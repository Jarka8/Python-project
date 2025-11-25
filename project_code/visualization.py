import plotly.express as px
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation


def correlation_scatterplot2(data, indicator_x, indicator_y):
    """
    Creates year-by-year scatterplots using two separate long-format indicator CSVs.

    indicator_x: path to CSV with long-format data for indicator X
    indicator_y: path to CSV with long-format data for indicator Y
    """
    # Get data for the two indicators
    df_x = data[indicator_x]
    df_y = data[indicator_y]

    # Detect value columns (only column that's not economy or year)
    val_x = [col for col in df_x.columns if col not in ["economy", "year"]][0]
    val_y = [col for col in df_y.columns if col not in ["economy", "year"]][0]

    # Merge on economy + year
    merged = df_x.merge(
        df_y, on=["economy", "year"], how="inner"
    )  # inner join to keep only matching entries

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
            x=val_x,
            y=val_y,
            hover_name="economy",
            title=f"{indicator_x} vs {indicator_y} ({yr})"
        )
        figs[yr] = fig

    return figs

def correlation_scatterplot(data, indicator_x, indicator_y):
    """
    Creates year-by-year scatterplots using two separate long-format indicator CSVs.
    """
    # Get data for the two indicators
    df_x = data[indicator_x].copy()
    df_y = data[indicator_y].copy()
    
    # Detect value columns
    val_x = [col for col in df_x.columns if col not in ["economy", "year"]][0]
    val_y = [col for col in df_y.columns if col not in ["economy", "year"]][0]
    
    # Rename the value columns to avoid conflicts during merge
    df_x = df_x.rename(columns={val_x: f"{indicator_x}_value"})
    df_y = df_y.rename(columns={val_y: f"{indicator_y}_value"})
    
    # Merge on economy + year
    merged = df_x.merge(df_y, on=["economy", "year"], how="inner")
    
    # Remove missing values
    merged = merged.dropna(subset=[f"{indicator_x}_value", f"{indicator_y}_value"])
    
    # Create scatterplots for each year
    years = sorted(merged["year"].unique())
    figs = {}
    
    for yr in years:
        temp = merged[merged["year"] == yr]
        fig = px.scatter(
            temp,
            x=f"{indicator_x}_value",
            y=f"{indicator_y}_value",
            hover_name="economy",
            title=f"{indicator_x} vs {indicator_y} ({yr})",
            labels={
                f"{indicator_x}_value": indicator_x.replace("_", " ").title(),
                f"{indicator_y}_value": indicator_y.replace("_", " ").title()
            }
        )
        figs[yr] = fig
    
    return figs

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


