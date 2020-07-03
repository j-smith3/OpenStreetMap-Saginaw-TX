# OpenStreetMap Data Wrangling - Saginaw, TX

## Data Analysis Project - Udacity Data Analyst Nanodegree

This project belongs to [Udacity's Data Analyst Nanodegree](https://www.udacity.com/course/data-analyst-nanodegree--nd002). Below you'll find links to the rest of the Nanodegree projects.

- Intro to Data Analysis - [Part 1](https://github.com/j-smith3/Investigating_TMDb_Dataset) & [Part 2](https://github.com/j-smith3/Test_A_Perceptual_Phenomenon)
- [Exploratory Data Analysis](https://github.com/j-smith3/White-Wine-EDA)
- [Data Wrangling](https://github.com/j-smith3/OpenStreetMap-Saginaw-TX)
- [Machine Learning](https://github.com/j-smith3/Enron_Fraud_Detection)
- [Data Visualization](https://github.com/j-smith3/Baseball-EDA-Visualization)

This project was developed in 2020 and is no longer maintained.

## About
This project investigated the OpenStreetMap data for my home town, Saginaw Texas. The OpenStreetMap data can be found [here](https://www.openstreetmap.org/relation/6571681). My project used this data, wrangled it into a cleaner format, then stored it into a SQLite database for further queries. 

## Usage
This project can be recreated by doing then following:

- Download OSM data [here](https://www.openstreetmap.org/relation/6571681) or use ```sample.osm``` for a small sample of the original OSM file

- Execute ```data.py``` to refine data and create csv files 

- Execute ```sql_db_creator.py``` to load csv files into a SQLlite database
