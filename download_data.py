"""
Script to downlaod data from open-meteo API
"""

import pandas as pd
import json
import time
import requests


def get_data(row: pd.Series):
    """
    Retrieve hourly temperature forecast data for a specific location using Open Meteo API.

    Parameters
    ----------
    row : pandas.Series
        A pandas Series representing a row of a DataFrame containing location information.
        It should have the following columns: 'lat', 'long', and 'name'.

    Returns
    -------
    pandas.DataFrame
        A DataFrame containing hourly temperature forecast data for the specified location.
        The DataFrame includes columns for timestamp, temperature at 2 meters, and the 'districts' column
        indicating the name of the location.

    Raises
    ------
    ValueError
        If the input row is missing the required columns: 'lat', 'long', or 'name'.
    requests.exceptions.RequestException
        If there is an issue with making the API request.
    json.JSONDecodeError
        If there is an issue decoding the JSON response from the API.
    """
    response = requests.get(
        f"https://api.open-meteo.com/v1/forecast?latitude={row.lat}&longitude={row.long}&hourly=temperature_2m&timezone=auto&past_days=92&forecast_days=1"
    )
    tmp = pd.DataFrame()
    if response.status_code == 200:
        try:
            weather_data = response.json()
            tmp = pd.DataFrame(data=weather_data["hourly"])
            tmp["districts"] = row["name"]
        except json.JSONDecodeError:
            print(f"Error decoding JSON for district: {row['name']}")
    return tmp

# ============================================
# Section 1: Download data
# ============================================


FILE_DIR = 'data/bd-districts.json'
AVG_TEMP_DIR = 'data/avg.csv'
FORECAST_TEMP_DIR = 'data/forecast.csv'

# Load the JSON data from the file with explicit encoding
with open(FILE_DIR, 'r', encoding='utf-8') as file:
    data = json.load(file)

# Flatten the "districts" key using json_normalize
df = pd.json_normalize(data, 'districts')

# Calculate the average temperature for each district and sort them
avg_temperatures_data = {}
temp_df = pd.DataFrame()
for _, data_row in df.iterrows():
    data = get_data(data_row)
    temp_df = pd.concat([temp_df, data], ignore_index=True)


# ============================================
# Section 2: Get data for 1st task
# ============================================

# filter based on 2 PM
temp_df["time"] = pd.to_datetime(temp_df["time"])
filtered_df = temp_df[temp_df['time'].dt.hour == 14]

# Calculate the average temperature for each city
average_temperatures = filtered_df.groupby(
    'districts')['temperature_2m'].mean().reset_index()
sorted_df = average_temperatures.sort_values(
    by='temperature_2m', ascending=True)

sorted_df.head(10).to_csv(AVG_TEMP_DIR, index=False)

# ============================================
# Section 3: Get data for 2nd task
# ============================================
filtered_df = temp_df[temp_df["districts"] == "Dhaka"]
grouped_by_date = filtered_df.groupby(temp_df['time'].dt.date)[
    'temperature_2m'].mean().reset_index()
grouped_by_date.to_csv(FORECAST_TEMP_DIR, index=False)
