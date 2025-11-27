"""
This module contains function for merging the selected indicators into one 
DataFrame and also selects the value column
"""

def merge_indicators(data, indicators: list):
    """
    Merges data for indicators provided in a list based on ['economy', 'year'].
    Returns:
        merged_df (DataFrame): merged and cleaned dataset
        value_cols (dict): indicator → detected value column
    """
    # Load dataframe for the first indicator
    df = data[indicators[0]].copy()
    
    # Detect the value column (only non economy/year column)
    val_cols = {
        ind : [c for c in data[ind].columns if c not in ["economy", "year"]][0]
        for ind in indicators
    }

    # Merge the datasets for all indicators
    for ind in indicators[1:]:
        df = df.merge(data[ind], on=["economy", "year"], how="inner")

    # Drop missing rows
    df = df.dropna(subset=val_cols.values())

    return df, val_cols