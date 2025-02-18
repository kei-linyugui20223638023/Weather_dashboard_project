from fasthtml.common import Strong, fast_app, serve, Titled, Div, P, Img, H1, H2, H3, A, Form, Label, Input, Button, Script, Ul, Li  
# Explicit import to satisfy mypy
import httpx
from fastapi import FastAPI, HTTPException, Query
import matplotlib.pyplot as plt
import base64
from io import BytesIO
import numpy as np
from datetime import datetime, timedelta
import logging
from urllib.parse import unquote
import requests
from flask import Flask, jsonify, abort, request, url_for


from getdata import get_weather_now, get_weather_today, get_weather_five_days
from processingdata import processing_data_now, processing_data_today, processing_data_five_days
from visualization import create_temperature_progressbar, create_humidity_gauge, create_wind_rose, create_temperature_chart, create_precipitation_chances_pie_charts, create_weather_forecast_table
from autolocation_process import get_city_name_auto
from get_icon import get_weather_icon
from restful_api import create_api, generate_api_url

app, rt = fast_app()

# FastHTML routes 
@rt("/")
def get():
    """
    Render the home page with a search form for weather queries.
    
    Returns:
        Titled: A titled HTML page with a search form and instructions.
    """
    
    # Add a search page with automatic location feature
    search_form = Form(action="/weather", method="get")(
        Label("Location Input:"),
        Input(type="text", name="city_name", id="locationInput"),
        Input(type="submit", value="Get Weather"),
        Button(type="button", onclick="getLocation()")("Auto Locate"),
        Script("""
            function getLocation() {
                if (navigator.geolocation) {
                    navigator.geolocation.getCurrentPosition(
                        function(position) {
                            var coordinates = position.coords.latitude.toFixed(4) + ", " + position.coords.longitude.toFixed(4);
                            // Send a request to the server to get the city name
                            fetch('/get_city_name_auto?coordinates=' + coordinates)
                                .then(response => response.text())
                                .then(cityName => {
                                    document.getElementById("locationInput").value = cityName;
                                })
                                .catch(error => {
                                    alert("Unable to obtain city name, please try again later.");
                                });
                        },
                        function(error) {
                            alert("Unable to obtain location information, please ensure location permissions are granted. Error code: " + error.code);
                        }
                    );
                } else {
                    alert("Your browser does not support geolocation.");
                }
            }
        """)
    )
    
    instructions = Div(
        P("Instructions:"),
        Ul(
            Li("Directly enter the city name to search for weather (e.g., Beijing)"),
            Li("Or click the 'Auto Locate' button to get the current location coordinates (location permission required)"),
        )
    )
    
    return Titled("Weather Query and Dashboard App", 
        Div(
            instructions,
            search_form
        )
    )

@rt("/get_city_name_auto")
def get_city_name_auto_view(coordinates: str = Query(...)):
    """
    Get the city name based on geographic coordinates.
    
    Args:
        coordinates (str): Geographic coordinates in the format "latitude, longitude".
        
    Returns:
        str: The name of the city corresponding to the given coordinates.
    """
    
    city_name = get_city_name_auto(coordinates)
    return city_name

@rt("/weather")
def weather(city_name: str = Query(...)):
    
    """
    Retrieve and display weather data for a specified city.
    
    Args:
        city_name (str): The name of the city for which to retrieve weather data.
        
    Returns:
        Titled: A titled HTML page displaying various weather-related charts and tables.
    """
    # Current data
    weather_data_now = get_weather_now(city_name)
    temperature, humidity, weather_description, city, icon_code, icon_url = processing_data_now(weather_data_now)

    # Create progress bars and humidity gauges
    temp_progressbar = create_temperature_progressbar(temperature)
    humidity_gauge = create_humidity_gauge(humidity)
    
    # Today data
    weather_data_today = get_weather_today(city_name)
    wind_speeds, wind_directions = processing_data_today(weather_data_today)
    
    # Create wind rose
    wind_rose = create_wind_rose(wind_speeds, wind_directions)

    # Five days forecast data
    weather_data_five_days = get_weather_five_days(city_name)    
    daily_highs, daily_lows, daily_averages, dates, icons, conditions_five_days, precipitation_chances = processing_data_five_days(weather_data_five_days)
    
    # Create temperature chart
    temperature_chart = create_temperature_chart(daily_highs, daily_lows, daily_averages, dates)
    
    # Create precipitation chances chart
    precipitation_chances_chart = create_precipitation_chances_pie_charts(precipitation_chances, dates)
    
    # Create weather forecast table
    weather_forecast_table = create_weather_forecast_table(icons, conditions_five_days, dates)
    
    # Extract url information
    now_url, today_url, five_days_url = generate_api_url(city)

    weather_html = Div(
        Div(
            # The first row of the dashboard
            Div(
                H1(f"Current Weather"),
                Div(
                    Img(src=icon_url, alt=weather_description, 
                        style="width:100px; height:100px; margin-right: 20px;"),
                    H2(f"Condition: {weather_description.capitalize()}", 
                      style="font-size: 20px; color: #666; margin: 0;"),
                    style="display: flex; align-items: center; margin-bottom: 20px;"
                ),
                style="grid-column: 1;"
            ),
            Div(
                H2("Temperature", style="font-size: 18px; color: #333; margin-bottom: 10px;"),
                P(f"{temperature}°C", style="font-size: 36px; margin: 0 0 10px 0; color: #2196F3;"),
                Img(src=f"data:image/png;base64,{temp_progressbar}", 
                    style="width:70%; height: 80px; object-fit: cover;"),
                style="grid-column: 2; padding-right: 20px;"
            ),
            Div(
                H2("Humidity", style="font-size: 18px; color: #333; margin-bottom: 10px;"),
                Img(src=f"data:image/png;base64,{humidity_gauge}", 
                    style="width:100%; height:150px; object-fit: contain;"),
                style="grid-column: 3;"
            ),
            style="display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 20px;"
        ),
        Div(
            # The second row of the dashboard
            Div(
                H2("Wind Rose Today", style="margin-bottom: 15px;"),
                Img(src=f"data:image/png;base64,{wind_rose}",
                    style="width: 100%; height: 210px; object-fit: contain;"),
                style="grid-column: 1;"
            ),
            Div(
                H2("5 Days Weather Forecast", style="margin-bottom: 15px;"),
                Img(src=f"data:image/png;base64,{weather_forecast_table}",
                    style="width: 100%; height: 250px; object-fit: contain;"),
                style="grid-column: 2; padding-right: 20px;"
            ),
            style="display: grid; grid-template-columns: 1fr 1fr; gap: 20px; margin-top: 20px;"
        ),
        Div(
            # The third row of the dashboard
            Div(
                H2("Temperature Forecast", style="margin-bottom: 15px;"),
                Img(src=f"data:image/png;base64,{temperature_chart}",
                    style="width: 100%; height: 250px; object-fit: contain;"),
                style="grid-column: 1;"
            ),
            Div(
                H2("Precipitation Chances", style="margin-bottom: 15px;"),
                Img(src=f"data:image/png;base64,{precipitation_chances_chart}",
                    style="width: 100%; height: 250px; object-fit: contain;"),
                style="grid-column: 2; padding-right: 20px;"
            ),
            style="display: grid; grid-template-columns: 1fr 1fr; gap: 20px; margin-top: 20px;"
        ),
        Div(
            # API
            Div(
                H3("API Information"),
                Div(
                    Strong(f"Now data API URL of {city_name}: {now_url}"),
                    style="font-weight: bold; color: black; margin-bottom: 10px; font-size: 16px;"
                ),
                Div(
                    Strong(f"Today data API URL of {city_name}: {today_url}"),
                    style="font-weight: bold; color: black; margin-bottom: 10px; font-size: 16px;"
                ),
                Div(
                    Strong(f"Forecast five days data API URL of {city_name}: {five_days_url}"),
                    style="font-weight: bold; color: black; margin-bottom: 10px; font-size: 16px;"
                ),
                Div(
                    f"Tips: The present weather data API URL is not working because your server is running the main program to present the weather data. If you want to use the API interface, please copy the name of the city you want to get, close the main program and run the make_API_runnable.py file and paste the name of the city you need to get into the input of that program.",
                    style="color: red; font-size: 12px; margin-top: 20px; text-align: center;"
                ),
                style="display: flex; flex-direction: column; align-items: center; padding: 20px; background-color: #f0f0f0;"
            ),
            style="margin-top: 20px;"
        ),
        Div(
            # 'return to home' button
            Div(
                A(href="/", style="display:inline-block; padding:12px 24px; border-radius:5px; text-decoration:none; color:#fff; background-color:#2196F3; transition:0.3s;")("Return to Home"),
                style="text-align:center; margin-top:20px;"
            ),
            style="text-align:center;"
        ),
        style="max-width: 1200px; margin: 0 auto; padding: 20px; display: flex; flex-direction: column;"
    )
    
    return Titled(f"Weather in {city}", weather_html)

serve() # run the app
