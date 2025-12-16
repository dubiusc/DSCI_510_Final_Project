# DSCI_510_Final_Project
This is a repository to submit the final project for the course DSCI 510 offered by USC

# Project Title: How are population statistics and weather variables correlated with air pollution levels across major global cities?

## Team Members:
1. Dubi Sao [3931757486], dsao@usc.edu
2. Manasa Vijayaraghavan [2685584788], mvijayar@usc.edu

## Overview of the Project:
 
The project examines correlations between population statistics, weather variables, and air pollution levels in major global cities. Air Quality Index (AQI) values are calculated using official U.S. EPA formulas derived from pollutant concentrations, and subsequent statistical analyses and visualizations are conducted.

## Installation and Requirements
1. Create and activate a virtual environment
```bash
python3 -m venv venv
source venv/bin/activate # macOS/Linux
venv\Scripts\activate # Windows
3. Install dependencies
   pip install -r requirements.txt

## Data Collection

Raw data is obtained from the following sources:

1. World Population Review: city names and population statistics (web scraping)
2. Nominatim (OpenStreetMap): geographic coordinates (API)
3. Open-Meteo Weather API: temperature, wind speed, wind direction
4. Open-Meteo Air Quality API: PM2.5, PM10, NO₂, and O₃ concentrations

To collect data, run:
python src/get_data.py
This script saves raw datasets to the data/raw/ directory.

## Data Cleaning

The data cleaning process includes:

1. Converting relevant columns to numeric types
2. Removing missing values
3. Eliminating duplicate city entries
4. Standardizing column formats

To clean the data, run:
python src/clean_data.py
Cleaned datasets are saved in data/processed/.

## Analysis and AQI Computation

AQI values are computed programmatically using official U.S. EPA breakpoint formulas based on PM2.5 concentrations. The analysis includes:

1. AQI calculation and categorical classification
2. Grouped statistics by population size and temperature category
3. Correlation analysis among AQI, pollutants, and weather variables
4. Ranking cities by pollution severity

Run the analysis using:
python src/analysis.py

## Visualization

The analysis script generates the following visualizations:

1. Correlation heatmap of AQI, pollutants, and weather variables
2. AQI distributions across temperature categories
3. Boxplots of AQI by city population group
4. Scatter plot of high AQI values versus temperature
5. Bar chart of the ten most polluted cities

All figures are saved to the results/ directory.

#Authors

##Dubi Sao
##Manasa Vijayaraghavan
