# run in a Python shell / at top of main.py for debugging
import os, sys
print("cwd:", os.getcwd())
print("sys.path[0]:", sys.path[0])
print("module exists:", os.path.exists("data_collection.py"))

from data_collection import collect_data
from data_cleaning import clean_data, split_data

if __name__ == "__main__":
    # Collect raw data from World Bank API
    collect_data()
    
    # Clean the collected data by removing low-coverage indicators and countries
    clean_data()
    
    # Split the cleaned data into separate files per indicator
    split_data()