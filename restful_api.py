# -*- coding: utf-8 -*-
"""
Created on Sun Feb 16 20:59:10 2025

@author: keiii
"""

from getdata import get_weather_now, get_weather_today, get_weather_five_days
from processingdata import processing_data_now, processing_data_today, processing_data_five_days

from flask import Flask, jsonify, abort, request, url_for
from flask import Response
from typing import Callable, Dict, List, Tuple

def create_api(city_name: str) -> Flask:
    """
    Creates a Flask application for weather data API.

    Args:
    city_name (str): The name of the city to fetch weather data for.

    Returns:
    Flask: A configured instance of the Flask application.
       Example response:
       <Flask 'restful_api'>
    
    Usage Example:
       >>>app = create_api('London')
       >>>app.run(debug=True, use_reloader=False)
      
      * Serving Flask app 'restful_api'
      * Debug mode: on
      * Running on http://localhost:5000 
      Press CTRL+C to quit
      
      (and then you can check the API through visiting the website http://localhost:5000/weatherdashboard/api/v1.0/weatherdatas) 
    """
    app = Flask(__name__)

    # Set necessary configuration items
    app.config['SERVER_NAME'] = 'localhost:5000'
    app.config['APPLICATION_ROOT'] = '/'
    app.config['PREFERRED_URL_SCHEME'] = 'http'

    # Current data
    weather_data_now = get_weather_now(city_name)
    temperature, humidity, weather_description, city, icon_code, icon_url = processing_data_now(weather_data_now)

    # Today data
    weather_data_today = get_weather_today(city_name)
    wind_speeds, wind_directions = processing_data_today(weather_data_today)

    # Five days data 
    weather_data_five_days = get_weather_five_days(city_name)
    daily_highs, daily_lows, daily_averages, dates, icons, conditions_five_days, precipitation_chances = processing_data_five_days(weather_data_five_days)

    now_data = {'city': city,
                'temperature': temperature,
                'humidity': humidity,
                'weather_description': weather_description,
                'icon_code': icon_code,
                'icon_url': icon_url}

    today_data = {'city': city,
                  'wind_speeds': wind_speeds,
                  'wind_directions': wind_directions}

    forecast_five_days_data = {'city': city,
                               'daily_highs': daily_highs,
                               'daily_lows': daily_lows,
                               'daily_averages': daily_averages,
                               'dates': dates,
                               'icons': icons,
                               'conditions_five_days': conditions_five_days,
                               'precipitation_chances': precipitation_chances}

    weatherdatas = [
        {
            'id': 1,
            'title': 'Now Data',
            'data': now_data
        },
        {
            'id': 2,
            'title': 'Today Data',
            'data': today_data
        },
        {
            'id': 3,
            'title': 'Forecast Five Days Data',
            'data': forecast_five_days_data
        }
    ]

    @app.route('/weatherdashboard/api/v1.0/weatherdatas/<int:weatherdata_id>', methods=['GET'])
    def get_weatherdata(weatherdata_id: int) -> Callable:
        """
        Retrieves specific weather data based on the given ID.

        Args:
        weatherdata_id (int): The ID of the weather data needed.

        Returns:
        jsonify: JSON response containing the requested weather data.
        """
        weatherdata = list(filter(lambda t: t['id'] == weatherdata_id, weatherdatas))
        if len(weatherdata) == 0:
            abort(404)
        return jsonify({'weatherdata': weatherdata[0]})

    @app.route('/weatherdashboard/api/v1.0/weatherdatas', methods=['POST'])
    def create_weatherdata() -> Response :
        """
        Creates a new weather data record.

        Returns:
        jsonify: JSON response containing the newly created weather data along with a 201 status code.
        """
        if not request.json or not 'title' in request.json:
            abort(400)
       
        last_id = weatherdatas[-1]['id']
        
        if not isinstance(last_id, int):
            abort(500, description="Invalid type for 'id' in weatherdatas.")
        
        weatherdata = {
            'id': last_id + 1,
            'title': request.json['title'],
            'data': request.json.get('data', "")
        }
        weatherdatas.append(weatherdata)
        return jsonify({'weatherdata': weatherdata}, status=201)

    @app.route('/weatherdashboard/api/v1.0/weatherdatas/<int:weatherdata_id>', methods=['PUT'])
    def update_weatherdata(weatherdata_id: int) -> Callable:
        """
        Updates a weather data record for a specific ID.

        Args:
        weatherdata_id (int): The ID of the weather data to be updated.

        Returns:
        jsonify: JSON response containing the updated weather data.
        """
        weatherdata = list(filter(lambda t: t['id'] == weatherdata_id, weatherdatas))
        if len(weatherdata) == 0:
            abort(404)
        if not request.json:
            abort(400)
        if 'title' in request.json and type(request.json['title']) != str:
            abort(400)
        if 'data' in request.json and type(request.json['data']) is not dict:
            abort(400)
        weatherdata[0]['title'] = request.json.get('title', weatherdata[0]['title'])
        weatherdata[0]['data'] = request.json.get('data', weatherdata[0]['data'])
        return jsonify({'weatherdata': weatherdata[0]})

    @app.route('/weatherdashboard/api/v1.0/weatherdatas/<int:weatherdata_id>', methods=['DELETE'])
    def delete_weatherdata(weatherdata_id: int) -> Callable:
        """
        Deletes a weather data record for a specific ID.

        Args:
        weatherdata_id (int): The ID of the weather data to be deleted.

        Returns:
        jsonify: JSON response containing the result of the deletion operation.
        """
        weatherdata = list(filter(lambda t: t['id'] == weatherdata_id, weatherdatas))
        if len(weatherdata) == 0:
            abort(404)
        weatherdatas.remove(weatherdata[0])
        return jsonify({'result': True})

    def make_public_weatherdata(weatherdata: dict) -> dict:
        """
        Converts weather data into a public format by adding URI links.

        Args:
        weatherdata (dict): The dictionary of weather data to be converted.

        Returns:
        dict: The converted dictionary of weather data including URI links.
        """
        new_weatherdata = {}
        for key in weatherdata:
            if key == 'id':
                new_weatherdata['uri'] = url_for('get_weatherdata', weatherdata_id=weatherdata['id'], _external=True)
            else:
                new_weatherdata[key] = weatherdata[key]
        return new_weatherdata

    @app.route('/weatherdashboard/api/v1.0/weatherdatas', methods=['GET'])
    def get_weatherdatas() -> Callable:
        """
        Retrieves all weather data records.

        Returns:
        jsonify: JSON response containing all weather data records.
        """
        return jsonify({'weatherdatas': list(map(make_public_weatherdata, weatherdatas))})

    return app

def generate_api_url(city_name: str) -> tuple:
    """
    Generates different endpoint URLs for the weather data API of a specific city.

    Args:
    city_name (str): The name of the city to generate URLs for.

    Returns:
    tuple: Contains URLs for real-time data, today's data, and five-day forecast data.
        Example response:
        ('http://localhost:5000/weatherdashboard/api/v1.0/weatherdatas/1', 'http://localhost:5000/weatherdashboard/api/v1.0/weatherdatas/2', 'http://localhost:5000/weatherdashboard/api/v1.0/weatherdatas/3')
    
    Usage Example:
        >>> generate_api_url('London')
        ('http://localhost:5000/weatherdashboard/api/v1.0/weatherdatas/1', 'http://localhost:5000/weatherdashboard/api/v1.0/weatherdatas/2', 'http://localhost:5000/weatherdashboard/api/v1.0/weatherdatas/3')
    """
    app = create_api(city_name)
    
    with app.app_context():
        now_url = url_for('get_weatherdata', weatherdata_id=1, _external=True)
        today_url = url_for('get_weatherdata', weatherdata_id=2, _external=True)
        five_days_url = url_for('get_weatherdata', weatherdata_id=3, _external=True)

    return now_url, today_url, five_days_url
    
