"""
This module contains functions for the empirical analysis such as for
calculation of correlation, partial correlation and regression.
"""

import numpy as np
import statsmodels.formula.api as smf
from project_code.utils import merge_indicators


def calculate_correlations(data, indicator_x, indicator_y, year):
    """
    Calculates correlation coefficients for two indicators across all years.
    """
    # Merge the two indicators
    df, val_cols = merge_indicators(data, [indicator_x, indicator_y])

    # Detect value columns
    val_x = val_cols[indicator_x]
    val_y = val_cols[indicator_y]

    # Calculate correlations for each year
    df = df[df["year"] == year]
    corr = np.corrcoef(df[val_x], df[val_y])[0, 1]  # correlation of x and y

    return corr


def partial_corr(data, indicator_x, indicator_y, indicator_z, year):
    """
    Computes partial correlation between x and y controlling for z.
    """
    # Merge the three indicators
    df, val_cols = merge_indicators(data, [indicator_x, indicator_y, indicator_z])

    # Detect value columns
    val_x = val_cols[indicator_x]
    val_y = val_cols[indicator_y]
    val_z = val_cols[indicator_z]

    df = df[df["year"] == year]

    # Regular correlations
    corr_xy = np.corrcoef(df[val_x], df[val_y])[0, 1]
    corr_xz = np.corrcoef(df[val_x], df[val_z])[0, 1]
    corr_yz = np.corrcoef(df[val_y], df[val_z])[0, 1]

    # Partial correlation formula
    numerator = corr_xy - corr_xz * corr_yz
    denominator = np.sqrt((1 - corr_xz**2) * (1 - corr_yz**2))

    if denominator == 0:
        return np.nan  # avoid division by zero
    return numerator / denominator


def regression(data, dep_var, indep_vars: list, clustered=False):
    """
    Panel regression with country fixed effects (and optional clustered errors).
    """
    df, val_cols = merge_indicators(data, [dep_var] + indep_vars)

    dep_col = val_cols[dep_var]
    ind_cols = [val_cols[ind] for ind in indep_vars]

    formula = f"{dep_col} ~ {' + '.join(ind_cols)} + C(economy)"

    if clustered:
        model = smf.ols(formula=formula, data=df).fit(
            cov_type="cluster", cov_kwds={"groups": df["economy"]}
        )
    else:
        model = smf.ols(formula=formula, data=df).fit()

    return model
