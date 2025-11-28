"""
This module contains function for merging the selected indicators into one
DataFrame and also selects the value column
"""


def merge_indicators(data, indicators: list):
    """
    Merges data for indicators provided in a list based on ['economy', 'year'].
    """
    df_merged = None
    val_cols = {}

    for i, ind in enumerate(indicators):
        df = data[ind].copy()
        # Detect value column (exclude 'economy' and 'year')
        val_col = [c for c in df.columns if c not in ["economy", "year"]][0]

        # Rename value column to avoid collisions
        # In case user analyses 2 indicators in 2d scatterplot
        # but one of them is the third fixed indicator for 3d plot
        new_col = f"{val_col}_{i}"
        df = df.rename(columns={val_col: new_col})
        val_cols[ind] = new_col

        if df_merged is None:
            df_merged = df
        else:
            df_merged = df_merged.merge(df, on=["economy", "year"], how="inner")

    # Drop rows with missing values in any of the selected indicators
    df_merged = df_merged.dropna(subset=list(val_cols.values()))

    return df_merged, val_cols
