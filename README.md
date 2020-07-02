# OpenStreetMap-Saginaw-TX
Saginaw's OpenStreetMap data wrangling and analysis through SQL queries.

## About
This project investigated the OpenStreetMap data for my home town, Saginaw Texas. The OpenStreetMap data can be found [here](https://www.openstreetmap.org/relation/6571681). My project used this data, wrangled it into a cleaner format, then stored the data into a SQLite database. 

## Usage
This project can be recreated by doing then following:

- Download OSM data [here](https://www.openstreetmap.org/relation/6571681)

- Execute ```data.py``` to refine data and create csv files 

- Execute ```sql_db_creator``` to load csv files into a SQLlite database
