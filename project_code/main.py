from .data_collection import collect_data
from .data_cleaning import clean_data, split_data, make_long_format

if __name__ == "__main__":
    # Collect raw data from World Bank API
    collect_data()
    
    # Clean the collected data by removing low-coverage indicators and countries
    clean_data()
    
    # Split the cleaned data into separate files per indicator
    split_data()
    
    # Convert each cleaned indicator file to long format
    make_long_format()
    
    
    
    