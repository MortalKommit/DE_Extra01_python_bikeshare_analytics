# Udacity Side Project - Explore US Bikeshare Data

This project produces descriptive statistics using data from publicly available bikeshare datasets, sourced from the cities of  
Chicago, New York City and Washington, DC. The dataset for Chicago is provided by Divvy, the data for NYC is provided by Citi Bike,  
and Capital Bikeshare has provided the data from Washington.  
  
Some data wrangling has been performed on these datasets, data cleaning steps that include dropping missing or null values, deduplication  
and transformation to rename columns and restrict the dataset to only 6 specified columns:  
Start Time, End Time, Trip Duration, Start Station, End Station, User Type, Gender, Birth Year  

## Installation Instructions
1. [Optional] Create and activate a virtual environment with venv, python3 -m venv <virtual_environment_name>, source <virtual_environment_name>/bin/activate  
2. Install requirements with the given requirements.txt file: pip install -r requirements.txt 
3. Verify that the plotext library has been installed for this project.

## Notes
- This project uses plotext to plot bar charts for certain statistic-derived reports in the terminal.
- Plotext works best with a UNIX-like OS, as Windows has compatibility issues with color in the default terminal.
- Matplotlib would be a better option to generate reports/charts, however, since the environment for this project was a terminal-based workspace,  a CLI plot library was used.
- The plots look best when the terminal is maximized.
- Use the save (s) option when provided with the graph prompt to save the graph in html format.

## Possible Improvements
- Include all cities while analyzing data [Duplicate ride ids between city data will need to be handled]
- Plot stacked charts / multiple bar plots by city
- Exception handling with try/except to catch KeyErrors in case mode() or other methods return None
- Use matplotlib with pie charts, histograms

### Changelog 
1.1 August 2022
- Changed bikeshare data passing syntax to create_data_graph. The code would run in the worksapce(pandas 0.23.3), whose syntax  
differs in fetching datetime attributes, and selecting .loc columns.
- Changed bikeshare data passing syntax to create_data_graph. The code would run in the worksapce(pandas 0.23.3), whose syntax differs in fetching datetime attributes, and selecting .loc columns.
- Post Review : Changed function method calls and body to notify user if month is not present in dataset 