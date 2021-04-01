# Quick Weather Check

Running on https://quickweathercheck.herokuapp.com

## The app
A streamlit website/app showing the weather record/forcast for a given city. Inputs are the name a city, and two numbers: how many days of history you want to see and how many days of predictions.
Data is retrived through the API of https://www.metaweather.com (Python requests), stored in a pandas DataFrame object and shown by Plotly.

# Data presented
Show information includes historical meteorology data (up to 31 days back in time), prediction for the upcoming days (up to 5-10 days ahead, depending on availibility), simple graphs of temperature, wind information, air pressure and humidity, scatter plots of couples or triples of temperature, humidity and air pressure, and some tables of numerical values.
