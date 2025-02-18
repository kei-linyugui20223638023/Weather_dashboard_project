from fasthtml.common import Strong, fast_app, serve, Titled, Div, P, Img, H1, H2, H3, A, Form, Label, Input, Button, Script, Ul, Li  
import httpx
from fastapi import FastAPI, HTTPException, Query
import matplotlib.pyplot as plt
import base64
from io import BytesIO
import numpy as np
from datetime import datetime, timedelta
import logging
from urllib.parse import unquote

from getdata import get_weather_now, get_weather_today, get_weather_five_days

def processing_data_now(data_now: dict) -> tuple:
    """
    Processes the raw current weather data fetched from the OpenWeatherMap API for use in a weather dashboard.

    Args:
        data_now (dict): The raw current weather data in JSON format.

    Returns:
        tuple: A tuple containing the extracted weather information:
            - temp (float): The current temperature in degrees Celsius.
            - humidity (int): The current humidity percentage.
            - description (str): A brief description of the current weather conditions.
            - city (str): The city name.
            - icon_code (str): The OpenWeatherMap icon code representing the current weather.
            - icon_url (str): The URL of the weather icon image.
              Example response:
              (17.64, 64, 'overcast clouds', 'Guangzhou', '04d', 'http://openweathermap.org/img/wn/04d@2x.png')
                  
    Usage Example:
        >>> processing_data_now({'coord': {'lon': 113.25, 'lat': 23.1167}, 
                                 'weather': [{'id': 804, 'main': 'Clouds', 'description': 'overcast clouds', 'icon': '04d'}], 
                                 'base': 'stations', 
                                 'main': {'temp': 17.64, 'feels_like': 17.13, 'temp_min': 17.64, 'temp_max': 17.64, 'pressure': 1024, 'humidity': 64, 'sea_level': 1024, 'grnd_level': 1023},
                                 'visibility': 10000, 
                                 'wind': {'speed': 3.42, 'deg': 15, 'gust': 3.41}, 
                                 'clouds': {'all': 100}, 'dt': 1739844483, 
                                 'sys': {'country': 'CN', 'sunrise': 1739833059, 'sunset': 1739874273},
                                 'timezone': 28800, 
                                 'id': 1809858, 
                                 'name': 'Guangzhou',
                                 'cod': 200})
        (17.64, 64, 'overcast clouds', 'Guangzhou', '04d', 'http://openweathermap.org/img/wn/04d@2x.png')
    """

    # Extract the required information from the raw data
    temp = data_now['main']['temp']
    humidity = data_now['main']['humidity']
    description = data_now['weather'][0]['description']
    city = data_now['name']
    icon_code = data_now['weather'][0]['icon']
    icon_url = f"http://openweathermap.org/img/wn/{icon_code}@2x.png"

    return temp, humidity, description, city, icon_code, icon_url

def processing_data_today(data_today: dict) -> tuple:
    
    """
    Processes the raw weather data for today to extract wind speeds and directions.
    
    This function takes the raw weather data fetched for today and extracts the wind speeds
    and directions for each three-hour interval since the start of the day. It is intended
    to be used for creating a wind rose diagram for the current day.

    Args:
    data_today (dict): The raw weather forecast data for today in JSON format.

    Returns:
    tuple: A tuple containing two lists:
        - wind_speeds (List[float]): A list of wind speeds for each three-hour interval.
        - wind_directions (List[int]): A list of wind directions in degrees for each interval.
        Example response:
        ([3.35, 3.09, 2.58, 2.39, 1.53, 1.23, 1.98, 2.83], [12, 10, 8, 16, 59, 145, 135, 138])
            
        
    Usage Example:
        >>> processing_data_today({'cod': '200', 
                                   'message': 0, 
                                   'cnt': 8,
                                   'list': [{'dt': 1739847600, 'main': {'temp': 17.9, 'feels_like': 17.36, 'temp_min': 17.9, 'temp_max': 17.9, 'pressure': 1024, 'sea_level': 1024, 'grnd_level': 1023, 'humidity': 62, 'temp_kf': 0}, 'weather': [{'id': 804, 'main': 'Clouds', 'description': 'overcast clouds', 'icon': '04d'}], 'clouds': {'all': 100}, 'wind': {'speed': 3.35, 'deg': 12, 'gust': 3.23}, 'visibility': 10000, 'pop': 0, 'sys': {'pod': 'd'}, 'dt_txt': '2025-02-18 03:00:00'}, {'dt': 1739858400, 'main': {'temp': 18.2, 'feels_like': 17.64, 'temp_min': 18.2, 'temp_max': 18.8, 'pressure': 1023, 'sea_level': 1023, 'grnd_level': 1020, 'humidity': 60, 'temp_kf': -0.6}, 'weather': [{'id': 804, 'main': 'Clouds', 'description': 'overcast clouds', 'icon': '04d'}], 'clouds': {'all': 100}, 'wind': {'speed': 3.09, 'deg': 10, 'gust': 2.88}, 'visibility': 10000, 'pop': 0, 'sys': {'pod': 'd'}, 'dt_txt': '2025-02-18 06:00:00'}, {'dt': 1739869200, 'main': {'temp': 19.33, 'feels_like': 18.73, 'temp_min': 19.33, 'temp_max': 20.04, 'pressure': 1021, 'sea_level': 1021, 'grnd_level': 1019, 'humidity': 54, 'temp_kf': -0.71}, 'weather': [{'id': 804, 'main': 'Clouds', 'description': 'overcast clouds', 'icon': '04d'}], 'clouds': {'all': 96}, 'wind': {'speed': 2.58, 'deg': 8, 'gust': 2.74}, 'visibility': 10000, 'pop': 0, 'sys': {'pod': 'd'}, 'dt_txt': '2025-02-18 09:00:00'}, {'dt': 1739880000, 'main': {'temp': 20.09, 'feels_like': 19.49, 'temp_min': 20.09, 'temp_max': 20.09, 'pressure': 1021, 'sea_level': 1021, 'grnd_level': 1020, 'humidity': 51, 'temp_kf': 0}, 'weather': [{'id': 804, 'main': 'Clouds', 'description': 'overcast clouds', ……}]})
        ([3.35, 3.09, 2.58, 2.39, 1.53, 1.23, 1.98, 2.83], [12, 10, 8, 16, 59, 145, 135, 138])
    """
    
    # Extracting hourly data for today
    today = datetime.utcnow()
    today_start = datetime(today.year, today.month, today.day)
    today_hourly_data = data_today.get('list', [])
        
    # Checking if there is any data
    if not today_hourly_data:
        return Titled("Error", Div(P("No hourly data available for today.")))
    
    # Extracting wind speed and direction data
    wind_speeds = [hour['wind']['speed'] for hour in today_hourly_data]
    wind_directions = [hour['wind']['deg'] for hour in today_hourly_data]
    
    # Checking if wind data is valid
    if not wind_speeds or not wind_directions:
        return Titled("Error", Div(P("No wind data available for today.")))
    
    return wind_speeds, wind_directions


def processing_data_five_days(data_five_days: dict) -> tuple:
    
    """
    Processes the raw weather forecast data for the next five days to extract daily high, low, and average temperatures,
    dates, weather icons, weather conditions, and precipitation chances.
    
    This function processes the forecast data fetched from the OpenWeatherMap API, which includes weather data for
    every three hours over a five-day period. It calculates the daily high, low, and average temperatures, as well as
    the maximum precipitation chance for each day. It also extracts the weather condition descriptions and corresponding
    icons for each day.
    
    Args:
        data_five_days (dict): A dictionary containing the raw weather forecast data for the next five days.
    
    Returns:
        A tuple containing seven lists:
        - daily_highs (List[float]): List of daily high temperatures.
        - daily_lows (List[float]): List of daily low temperatures.
        - daily_averages (List[float]): List of daily average temperatures.
        - dates (List[str]): List of dates for the next five days in 'YYYY-MM-DD' format.
        - weather_icons (List[str]): List of weather icons corresponding to each day.
        - weather_conditions (List[str]): List of weather condition descriptions for each day.
        - precipitation_chances (List[float]): List of maximum precipitation chances for each day as a percentage.
        Example response:
        ([20.09, 23.97, 25.01, 24.38, 23], [17.9, 18.28, 19.53, 18.14, 17.17], [19.115, 20.33875, 21.46, 20.54375, 20.255], ['2025-02-18', '2025-02-19', '2025-02-20', '2025-02-21', '2025-02-22'], ['04d', '04d', '04d', '04d', '04d'], ['overcast clouds', 'overcast clouds', 'overcast clouds', 'overcast clouds', 'overcast clouds'], [0, 0, 0, 0, 0])
        
    Usage Example:
        >>>processing_data_five_days({'cod': '200',
                                      'message': 0, 
                                      'cnt': 40, 
                                      'list': [...]}))  
        ([20.09, 23.97, 25.01, 24.38, 23], [17.9, 18.28, 19.53, 18.14, 17.17], [19.115, 20.33875, 21.46, 20.54375, 20.255], ['2025-02-18', '2025-02-19', '2025-02-20', '2025-02-21', '2025-02-22'], ['04d', '04d', '04d', '04d', '04d'], ['overcast clouds', 'overcast clouds', 'overcast clouds', 'overcast clouds', 'overcast clouds'], [0, 0, 0, 0, 0])
    """
    
    
    
    daily_highs = []
    daily_lows = []
    daily_averages = []
    dates = []
    weather_icons = []
    weather_conditions = []
    precipitation_chances = []

    # Obtain the current date and calculate the dates for the next 5 days
    current_date = datetime.now()
    dates = [(current_date + timedelta(days=i)).strftime('%Y-%m-%d') for i in range(5)]

    # Divide the data into daily sub-lists
    for i in range(0, len(data_five_days['list']), 8):  # Every 8 data points represent a day
        daily_temps = [entry['main']['temp'] for entry in data_five_days['list'][i:i+8]]
        daily_temps_max = [entry['main']['temp_max'] for entry in data_five_days['list'][i:i+8]]
        daily_temps_min = [entry['main']['temp_min'] for entry in data_five_days['list'][i:i+8]]
        daily_highs.append(max(daily_temps_max))
        daily_lows.append(min(daily_temps_min))
        daily_averages.append(sum(daily_temps) / len(daily_temps))

        # Obtain weather icons, conditions, and precipitation chances
        weather_icons.append(data_five_days['list'][i]['weather'][0]['icon'])
        weather_conditions.append(data_five_days['list'][i]['weather'][0]['description'])
        
        daily_precipitation = [entry['pop'] for entry in data_five_days['list'][i:i+8]]  # Average precipitation chance for each day
        precipitation_chances.append(max(daily_precipitation) * 100)  # Convert to percentage

    return daily_highs, daily_lows, daily_averages, dates, weather_icons, weather_conditions, precipitation_chances

