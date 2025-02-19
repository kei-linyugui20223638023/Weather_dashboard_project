import httpx
from httpx import get
from fastapi import FastAPI, HTTPException, Query
from fastapi.responses import HTMLResponse
import matplotlib.pyplot as plt
import numpy as np
import io
import base64
from datetime import datetime, timedelta

from typing import Dict

def get_weather_now(location: str) -> Dict:
    
    """
    Fetches current weather data for a given location using the OpenWeatherMap API.

    Args:
        location (str): The city name or location identifier for which to retrieve weather data.
                        For example, "London", "New York", or "Guangzhou".

    Returns:
        dict: A dictionary containing the current weather data in JSON format.
              Example response:
              {
                  'coord': {'lon': 113.25, 'lat': 23.1167},
                  'weather': [{'id': 804, 'main': 'Clouds', 'description': 'overcast clouds', 'icon': '04d'}],
                  'base': 'stations',
                  'main': {'temp': 17.64, 'feels_like': 17.13, 'temp_min': 17.64, 'temp_max': 17.64, 'pressure': 1024, 'humidity': 64, 'sea_level': 1024, 'grnd_level': 1023},
                  'visibility': 10000,
                  'wind': {'speed': 3.42, 'deg': 15, 'gust': 3.41},
                  'clouds': {'all': 100},
                  'dt': 1739843673,
                  'sys': {'country': 'CN', 'sunrise': 1739833059, 'sunset': 1739874273},
                  'timezone': 28800,
                  'id': 1809858,
                  'name': 'Guangzhou',
                  'cod': 200
              }

    Raises:
        HTTPException: If the OpenWeatherMap API request fails.

    Usage Example:
        >>> get_weather_now('guangzhou')
        {
            'coord': {'lon': 113.25, 'lat': 23.1167},
            'weather': [{'id': 804, 'main': 'Clouds', 'description': 'overcast clouds', 'icon': '04d'}],
            ...
        }
    """
    # OpenWeatherMap API configuration
    OPENWEATHERMAP_API_URL = "http://api.openweathermap.org/data/2.5/weather"
    OPENWEATHERMAP_API_KEY = "07097eccc08cd3f9c2d6186f6847cf89"  # Replace with your API key

    response = get(
        OPENWEATHERMAP_API_URL,
        params={"q": location, "appid": OPENWEATHERMAP_API_KEY, "units": "metric"},
    )
    if response.status_code != 200:
        raise HTTPException(status_code=400, detail="OpenWeatherMap API error")
    return response.json()




def get_weather_today(location: str) -> Dict:

    """
    Fetches today's weather data for a given location using the OpenWeatherMap API.

    Args:
        location (str): The city name or location identifier for which to retrieve weather data.
                        For example, "London", "New York", or "Guangzhou".

    Returns:
        dict: A dictionary containing the weather forecast data for today, with 8 different time slots, in JSON format.
              Example response:
              {
                  'cod': '200',
                  'message': 0,
                  'cnt': 8,
                  'list': [
                      {
                          'dt': 1739847600,
                          'main': {'temp': 17.9, 'feels_like': 17.36, 'temp_min': 17.9, 'temp_max': 17.9, 'pressure': 1024, 'sea_level': 1024, 'grnd_level': 1023, 'humidity': 62, 'temp_kf': 0},
                          'weather': [{'id': 804, 'main': 'Clouds', 'description': 'overcast clouds', 'icon': '04d'}],
                          'clouds': {'all': 100},
                          'wind': {'speed': 3.35, 'deg': 12, 'gust': 3.23},
                          'visibility': 10000,
                          'pop': 0,
                          'sys': {'pod': 'd'},
                          'dt_txt': '2025-02-18 03:00:00'
                      },
                      ...
                  ],
                  'city': {'id': 1809858, 'name': 'Guangzhou', ...}
              }

    Raises:
        HTTPException: If the OpenWeatherMap API request fails.

    Usage Example:
        >>> print(get_weather_today('guangzhou'))
        {
            'cod': '200',
            'message': 0,
            'cnt': 8,
            'list': [...],
            'city': {...}
        }
    """

    # OpenWeatherMap API configuration
    OPENWEATHERMAP_API_URL = "http://api.openweathermap.org/data/2.5/forecast"
    OPENWEATHERMAP_API_KEY = "07097eccc08cd3f9c2d6186f6847cf89"  # Replace with your API key

    response = get(
        OPENWEATHERMAP_API_URL,
        params={"q": location,
                "appid": OPENWEATHERMAP_API_KEY,
                "units": "metric",
                "cnt": 8,  # Fetch data for today with a 3-hour interval
                },
    )
    if response.status_code != 200:
        raise HTTPException(status_code=400, detail="OpenWeatherMap API error")
    return response.json()

def get_weather_five_days(location: str) -> Dict:
    
    """
    Fetches weather forecast data for the next 5 days for a given location using the OpenWeatherMap API.

    Args:
        location (str): The city name or location identifier for which to retrieve weather data.
                        For example, "London", "New York", or "Guangzhou".

    Returns:
        dict: A dictionary containing the weather forecast data for the next 5 days, with 40 different time slots, in JSON format.
              Example response:
              {
                  'cod': '200',
                  'message': 0,
                  'cnt': 40,
                  'list': [
                      {
                          'dt': 1739847600,
                          'main': {'temp': 17.9, 'feels_like': 17.36, 'temp_min': 17.9, 'temp_max': 17.9, 'pressure': 1024, 'sea_level': 1024, 'grnd_level': 1023, 'humidity': 62, 'temp_kf': 0},
                          'weather': [{'id': 804, 'main': 'Clouds', 'description': 'overcast clouds', 'icon': '04d'}],
                          'clouds': {'all': 100},
                          'wind': {'speed': 3.35, 'deg': 12, 'gust': 3.23},
                          'visibility': 10000,
                          'pop': 0,
                          'sys': {'pod': 'd'},
                          'dt_txt': '2025-02-18 03:00:00'
                      },
                      ...
                  ],
                  'city': {'id': 1809858, 'name': 'Guangzhou', ...}
              }

    Raises:
        HTTPException: If the OpenWeatherMap API request fails.

    Usage Example:
        >>> get_weather_five_days('guangzhou')
        {
            'cod': '200',
            'message': 0,
            'cnt': 40,
            'list': [...],
            'city': {...}
        }
    """

    # OpenWeatherMap API configuration
    OPENWEATHERMAP_API_URL = "http://api.openweathermap.org/data/2.5/forecast"
    OPENWEATHERMAP_API_KEY = "07097eccc08cd3f9c2d6186f6847cf89"  # Replace with your API key

    response = get(
        OPENWEATHERMAP_API_URL,
        params={
            "q": location,
            "appid": OPENWEATHERMAP_API_KEY,
            "units": "metric",
            "cnt": 40,  # Fetch data for the next 5 days, with a 3-hour interval
        },
    )
    if response.status_code != 200:
        raise HTTPException(status_code=400, detail="OpenWeatherMap API error")
    return response.json()
