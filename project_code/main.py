"""
This module is used to execute the data collection and cleaning functions
prior to running the streamlit for a quicker execution of the dashboard.
"""

from project_code.data_collection import collect_data
from project_code.data_cleaning import clean_data, split_data, long_format_data

if __name__ == "__main__":
    # Collect raw data from World Bank API
    collect_data()

    # Clean the collected data by removing low-coverage indicators and countries
    clean_data()

    # Split the cleaned data into separate files per indicator
    split_data()

    # Convert each cleaned indicator file to long format
    long_format_data()
