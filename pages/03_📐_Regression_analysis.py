"""
Dashboard page showing the regression.
"""

import streamlit as st
from project_code.data_cleaning import load_indicator_data
from project_code.analysis import regression
from project_code.visualization import regression_summary_table, highlight_significant

st.set_page_config(page_title="The Wealth of Nations", layout="wide", page_icon="🗺️")

st.title("📐 Regression analysis")

# Load data
data = load_indicator_data(rename_countries=False)
indicators = list(data.keys())
indicator_display_names = {name: name.replace("_", " ").title() for name in indicators}

with st.expander("What is Regression Analysis?", expanded=False):
    st.markdown(
        """
    **Regression analysis** helps us understand the relationship between variables.
    - Does higher GDP lead to better health outcomes?
    - How does health expenditure relate to life expectancy?
    
    This specific regression model runs a **panel regression with country fixed effects**.
    - Controls for unchanging country characteristics (culture, geography, etc.)
    - Analyzes how changes in one variable relate to changes in another over time
    """
    )

with st.expander(" How to Read the Results Table", expanded=False):
    st.markdown(
        """
    **Variables**: The factors you selected to analyze
    - Y is the **dependent** variable, the one you want to analyse and see how other factors 
    influence it.
    - X is the **independent** variable, the one possibly influencing the dependent variable.

    Including multiple X variables (*control variables*) helps you:
    - **Isolate the true effect**: When studying how health spending affects life expectancy, 
    you should also control for GDP per capita, because wealthier countries tend to have 
    both higher health spending and longer life expectancy.
    - **Avoid biased results**: Without controls, you might incorrectly attribute an effect 
    to a variable when it's actually caused by variable another omitted one.
    
    With contorol variables looking at the outcomes of one means holding other constant: 
    The change in life expectancy given health expenditure, holding GDP unchanged.
    
    **Coefficients**: The estimated effect size
    - *Positive* = when X increases, Y tends to increase
    - *Negative* = when X increases, Y tends to decrease
    - The number shows how much Y changes for a 1-unit increase in X
    
    **Std. Error**: Measures uncertainty in the coefficient estimate 
    - The smaller it is the more precise the coefficient of given variable is.
    
    **t-value**: How many standard errors the coefficient is away from zero 
    - The larger its absolute value the stronger possibility of effect being significant.
    
    **P-value**: Probability the relationship is accidental
    - *< 0.05* = statistically significant (highlighted in green)
    - *< 0.01* = highly significant
    - *> 0.05* = not statistically significant
    
    **CI 2.5% and CI 97.5%**: The 95% confidence interval
    - We're 95% confident the true effect falls within this range
    - If the interval includes 0, the effect might not be real
    
    **Intercept**: The baseline value when all predictors are zero (often not meaningful to 
    interpret)
    
    **R² (R-squared)**: Measures how well your model explains the variation in the dependent 
    variable
    - Ranges from 0 to 1
    - *R² = 0.75* means your model explains 75% of the variation in Y
    - *Higher = better fit*, but adding more variables always increases R² (even random ones!)

    **Adjusted R²**: A modified version that penalizes adding unnecessary variables
    - Only increases if a new variable genuinely improves the model
    - *Always lower than R²* (or equal)
    - Preferred when using multiple control variables

    **Note**: In panel regressions with country fixed effects, R² can be very high (0.8-0.9+) 
    because fixed effects explain a lot of variation. Focus more on coefficient significance 
    and adjusted R² in this case.
    """
    )

# Let user select dependent variable
default_indicator = indicators.index("life_expectancy")
var_y = st.selectbox(
    "Select dependent variable:",
    options=indicators,
    format_func=lambda x: indicator_display_names[x],
    index=default_indicator,
)

# Let user select independent variables
available_for_x = [ind for ind in indicators if ind != var_y]
vars_x = st.multiselect(
    "Select independent variable(s):",
    options=[ind for ind in indicators if ind != var_y],
    format_func=lambda x: indicator_display_names[x],
)

# Cluster option
clustered = st.checkbox("Use clustered standard errors by country", value=False)

# Print the regression summary table
if vars_x and st.button("Run regression"):
    result = regression(data, var_y, vars_x, clustered=clustered)
    summary_df = regression_summary_table(result)

    st.subheader("Regression Results")

    # Show R2 and Adjusted R2
    st.markdown(
        f"""
    R² = {result.rsquared:.3f}
    \nAdjusted R² = {result.rsquared_adj:.3f}  
    """
    )

    st.dataframe(summary_df.style.apply(highlight_significant, axis=1))

    st.text(
        "The highlighted rows demonstate the variables with P-value < 0.05 which shows significance."
    )
