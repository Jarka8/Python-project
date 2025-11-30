# 🗺️ The Wealth of Nations
## Analysing Economic Environmental and Health Indicators

*Python class project for [Coding for Data Science] - [2025]*

This repository is used to create an interactive **Streamlit web application** for exploring global development indicators such as GDP per capita, CO₂ emissions, renewable energy, life expectancy, child mortality, pollution and more.

The dashboard provides:
- Choropleth world maps  
- 2D scatterplot with animation over the years option
- 3D scatterplot
- Regression analysis summary table

If you would like to see the outcome of the project and explore the app without downloading anything, having to have a code editor or knowing anything about coding, simply click on the link below. 😊

## https://wealth-of-nations-data-analysis.streamlit.app

However, if you are brave enough and wish to run this project by yourself follow these steps and I hope it will still work. 😅

Open your Python code editor (I use Visual Studio Code), in it open a folder where you want this to be downloaded at and **clone this repository** into your device by running following line in the terminal. 

```bash
git clone https://github.com/Jarka8/Python-project.git
```
❗️ Remember that for it to function properly all of these lines must be run in the terminal NOT inserted in the actual files.

Then **enter the project folder** with:
```bash
cd Python-project
```

**Create and activate a virtual environment** to download the required packages only in this environment where this project will be run and to not mess up with the packages downloaded in your global environment.
```bash
python3 -m venv venv
```

For macOS/Linux
```bash
source venv/bin/activate
```
For windows
```bash
.\venv\Scripts\activate
```

Next, **install all requirements** from the requirements.txt file.
```bash
pip install -r requirements.txt
```
Now everything should be ready for the **streamlit** to be run.
```bash
streamlit run _🌍_Global_overview.py
```
The app should automatically open in your browser.


## 📁 Project Structure
```
Python-project/
├── data/                         # Data files
│   ├── raw/                      # Raw data from World Bank API + backup file
│   └── cleaned/                  # Processed data
│       └── long/                 # Long-format data for analysis (will be created after running)
├── exploration_and_analysis/      
│   └── project_analysis.ipynb    # Jupyter Notebook with initial data exploration  
├── pages                         # Pages of the dashboard
│   ├── 01_🔎_Indicator_guide.py
│   ├── 02_📈_Scatterplots_and_correlations.py
│   └── 03_📐_Regression_analysis.py
├── _🌍_Global_overview.py        # Main dashboard page
├── project_code/                 # Core Python modules
│   ├── data_collection.py        # World Bank API data fetching
│   ├── data_cleaning.py          # Data processing and loading
│   ├── visualization.py          # Plotting functions
│   ├── analysis.py               # Computing correlations and regressing
│   ├── utils.py                  # Merging chosen indicators into df
│   └── main.py                   # Setup pipeline
├── requirements.txt              # Python dependencies
├── README.md                     # This file
└── .gitignore                    # What not to track by git
```


## 📊 Data Source

All data is sourced from the **[World Bank Open Data](https://data.worldbank.org/)** portal via their Python API.

**15 Indicators:**
- **Economy:** GDP per capita, GDP growth, Carbon intensity of GDP
- **Health:** Life expectancy, Child mortality, Health expenditure (per capita and % of GDP)
- **Environment:** CO₂ emissions, PM2.5 pollution, Greenhouse gasses emissions, Forest area, Renewable energy
- **Demographics:** Population, Urban population %, Population growth

**Time period:** 2000-2023  

**Countries:** 123 countries (with population > 5 million and no more than 30% missing data)

## 👩🏼‍💻 Author

**Jaroslava** ([Jarka8](https://github.com/Jarka8))  
*Data Science for Economics and Health - [Università degli Studi di Milano]*