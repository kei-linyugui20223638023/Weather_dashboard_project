# -*- coding: utf-8 -*-
"""
Created on Mon Feb 17 11:04:17 2025

@author: keiii
"""

from getdata import get_weather_now, get_weather_today, get_weather_five_days
from processingdata import processing_data_now, processing_data_today, processing_data_five_days
from restful_api import create_api

from flask import Flask, jsonify, abort, request, url_for

city_name = input('please input your city name :\n (You can get it by running the main programme and click auto locate)\n')
# Enter the city name to build the API interface for weather data of that city

app = create_api(city_name) # Create an instance of the Flask application to generate the interface
    
with app.app_context():   # Define the context for the Flask application instance to use
    now_url = url_for('get_weatherdata', weatherdata_id=1, _external=True)   # Extract related URLs
    today_url = url_for('get_weatherdata', weatherdata_id=2, _external=True)
    five_days_url = url_for('get_weatherdata', weatherdata_id=3, _external=True)

if __name__ == '__main__':       # Run the code to output the API URLs for the corresponding city
    print('\n Now data API URL:'+now_url)
    print('\n Today data API URL:'+today_url)
    print('\n Forecast five days data API URL:'+five_days_url)
    print('\n Now the API URL is available......')
    app.run(debug=True, use_reloader=False)    # Launch the application instance on the server to make the API effective

    
    

    
    