# -*- coding: utf-8 -*-
"""
Created on Mon Feb 10 13:51:47 2025

@author: keiii
"""

from fasthtml.common import *
import httpx
from fastapi import FastAPI, HTTPException, Query
import matplotlib.pyplot as plt
import base64
import io
from io import BytesIO
import numpy as np
from datetime import datetime, timedelta
from PIL import Image

from get_icon import get_weather_icon

def create_temperature_progressbar(temperature: float) -> str:
    """
    Creates a temperature progress bar image as a base64 encoded string.

    The function generates a horizontal progress bar that visually represents
    the given temperature within a predefined range from -30C to 50C.
    The progress bar includes a marker for 0C and labels for the minimum
    and maximum temperature limits.

    Args:
    - temperature (float): The temperature value to be represented on the progress bar.

    Returns:
    - str: A base64 encoded string of the progress bar image.

    Raises:
    - ValueError: If the temperature is outside the defined range of -30C to 50C.
    
    Usage Example:
        >>> create_temperature_progressbar(11.0)  
        It should return a Base64 encoding of a string type (specific example results are not displayed because the image converted to encoding is too long) 
    """

    length = 6
    width = 0.5
    maxtemp = 50
    mintemp = -30
    percentage = (temperature - mintemp) / (maxtemp - mintemp) * 100

    # Calculate the position of 0C within the range of -30 to 50
    zeroposition = (0 - mintemp) / (maxtemp - mintemp) * 100  # 37.5%

    fig, ax = plt.subplots(figsize=(length, width), dpi=100)
    ax.set_xlim(0, 100)
    ax.set_ylim(-1, 1)
    ax.axis('off')

    # Draw the progress bar
    ax.barh([0], [100], 1, color='#eeeeee')
    ax.barh([0], [percentage], 1, color='#2196F3')

    # Add a marker for 0C
    ax.axvline(zeroposition, ymin=0.4, ymax=0.6, color='white', linestyle='-', linewidth=2)
    ax.text(zeroposition, -1.8, '0°C', ha='center', va='top', fontsize=8, color='#666666')

    # Label the minimum and maximum temperature limits and the current temperature
    ax.text(0, -1.8, f'{mintemp}°C', ha='left', va='top', fontsize=6, color='#666666')
    ax.text(100, -1.8, f'{maxtemp}°C', ha='right', va='top', fontsize=6, color='#666666')
    ax.text(percentage, 1.5, f'{temperature:.1f}°C', ha='center', va='bottom', fontsize=8, color='#2196F3', fontweight='bold')

    buffer = BytesIO()
    fig.savefig(buffer, format='png', bbox_inches='tight', pad_inches=0.2)
    plt.close()
    return base64.b64encode(buffer.getvalue()).decode()


def create_humidity_gauge(humidity: float) -> str:
    
    """
    Create a humidity gauge image and return the corresponding base64 string.

    Args:
    humidity (float): The humidity value to be displayed on the gauge, ranging from 0 to 100.

    Returns:
    str: A base64 encoded string representing the humidity gauge image.

    Description:
    This function generates a semi-circular humidity gauge image with tick marks,
    labels, and a pointer indicating the current humidity level. The gauge's
    outline is drawn, along with the tick marks and labels for every 10%. The
    pointer is positioned according to the input humidity value. The humidity
    percentage is displayed in the center of the gauge. The image is saved in
    PNG format, encoded to base64, and returned as a string.
    
    Usage Example:
        >>> create_humidity_gauge(8.0)
        
        It should return a Base64 encoding of a string type (specific example results are not displayed because the image converted to encoding is too long) 

    """
    fig, ax = plt.subplots(figsize=(4, 3), dpi=100)
    ax.set_xlim(-1.2, 1.2)
    ax.set_ylim(-0.2, 1.2)
    ax.axis('off')

    # Draw the gauge outline (semi-circular)
    theta = np.linspace(np.pi, 0, 100)
    r = np.ones(100)
    ax.plot(np.cos(theta), np.sin(theta), color='#66CCFF', lw=4)

    # Add tick marks and labels
    for value in range(0, 101, 10):
        angle = np.pi - (value / 100) * np.pi
        # Major tick marks
        ax.plot([0.9*np.cos(angle), np.cos(angle)],
                [0.9*np.sin(angle), np.sin(angle)],
                color='#66CCFF', lw=3)  # Bold for major ticks
        # Tick labels
        if value % 20 == 0:
            ax.text(1.19*np.cos(angle), 1.19*np.sin(angle), f'{value}%',
                    ha='center', va='center', fontsize=10, color='#0000FF')  # Change to blue for every 20th label

    # Draw the pointer
    pointer_angle = np.pi - (humidity / 100) * np.pi
    ax.plot([0, 0.8*np.cos(pointer_angle)],  # Pointer length set to 0.8
            [0, 0.8*np.sin(pointer_angle)],
            color='#FF5722', lw=4, zorder=3)  # Bold
    # Add a circle for the pointer's pivot point
    ax.add_patch(plt.Circle((0, 0), 0.05, color='#FF5722', zorder=4))

    # Add the central humidity display
    ax.text(0, -0.15, f'{humidity}%', 
            ha='center', va='center', 
            fontsize=20, color='#FF5722', 
            fontweight='bold')

    buffer = BytesIO()
    fig.savefig(buffer, format='png', bbox_inches='tight', pad_inches=0.2)
    plt.close()
    return base64.b64encode(buffer.getvalue()).decode()



def create_wind_rose(wind_speeds: list, wind_directions: list) -> str:
    
    """
    Create a wind rose plot and return the corresponding base64 string.

    Args:
    wind_speeds (List[float]): A list of wind speeds.
    wind_directions (List[float]): A list of wind directions in degrees.

    Returns:
    str: A base64 encoded string representing the wind rose image.

    Description:
    This function takes wind speed and direction data to generate a wind rose plot
    in polar coordinates. The wind directions are binned into sectors of 22.5 degrees,
    and the frequency of occurrence for each sector is calculated. The plot is then
    drawn with bars representing the frequency of each wind direction. The resulting
    image is converted to a base64 encoded string for easy embedding in web pages or
    other applications.
    
    Usage Example:
        >>> create_wind_rose([3.35, 3.09, 2.58, 2.39, 1.53, 1.23, 1.98, 2.83],
                             [12, 10, 8, 16, 59, 145, 135, 138]) 
        
        It should return a Base64 encoding of a string type (specific example results are not displayed because the image converted to encoding is too long) 
    """
    if not wind_speeds or not wind_directions:
        raise ValueError("No wind data available to plot.")
    
    fig, ax = plt.subplots(figsize=(7, 7), subplot_kw={'polar': True})
    # Set the zero location to North
    # Set the direction of increasing theta to clockwise
    
    # Calculate the frequency of wind directions
    bins = np.arange(0, 360, 22.5)
    hist, bin_edges = np.histogram(wind_directions, bins=bins)

    bin_centers = (bin_edges[:-1] + bin_edges[1:]) / 2
    theta = np.deg2rad(bin_centers) - np.pi / 2
    # Set the zero location to North
    # Set the direction of increasing theta to clockwise
    
    # Plot the wind rose
    ax.bar(theta, hist, width=np.deg2rad(22.5), color='blue', alpha=0.7)
    
    ax.set_xticks(np.deg2rad(np.arange(0, 360, 45)))
    ax.set_xticklabels(['E', 'NE', 'N', 'NW', 'W', 'SW', 'S', 'SE'])
    
    # Convert the image to base64 encoding
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    image_base64 = base64.b64encode(buf.read()).decode('utf-8')
    plt.close(fig)
    
    return image_base64


def create_temperature_chart(daily_highs: list, daily_lows: list, 
                            daily_averages: list, dates: list) -> str:
    """
    Create a temperature chart and return the corresponding base64 string.

    Args:
    daily_highs (List[float]): A list of daily high temperatures.
    daily_lows (List[float]): A list of daily low temperatures.
    daily_averages (List[float]): A list of daily average temperatures.
    dates (List[str]): A list of dates corresponding to the temperature data.

    Returns:
    str: A base64 encoded string representing the temperature chart image.

    Description:
    This function takes lists of daily high, low, and average temperatures along with dates,
    and creates a temperature chart that includes line plots for high and low temperatures
    and a bar chart for average temperatures. The chart is for a 5-day period.
    
    Usage Example:
        >>> create_temperature_chart([20.09, 23.97, 25.01, 24.38, 23],
                                     [17.9, 18.28, 19.53, 18.14, 17.17],
                                     [19.115, 20.33875, 21.46, 20.54375, 20.255],
                                     ['2025-02-18', '2025-02-19', '2025-02-20', '2025-02-21', '2025-02-22']) 
        
        It should return a Base64 encoding of a string type (specific example results are not displayed because the image converted to encoding is too long) 
   """

    # Plotting the temperature chart
    fig, ax1 = plt.subplots(figsize=(6, 3.5))

    # Line plots for daily high and low temperatures
    ax1.plot(range(5), daily_highs, label='Daily High', color='red', marker='o')
    ax1.plot(range(5), daily_lows, label='Daily Low', color='blue', marker='o')
    ax1.set_xlabel('Date')
    ax1.set_ylabel('Temperature (°C)', color='black')
    ax1.set_xticks(range(5))
    ax1.set_xticklabels(dates, rotation=45, ha='right')
    ax1.tick_params(axis='y', labelcolor='black')
    ax1.legend(loc='upper left')

    # Bar chart for average temperature
    ax2 = ax1.twinx()
    ax2.bar(range(5), daily_averages, color='green', alpha=0.6, label='Average Temperature')
    ax2.set_ylabel('Average Temperature (°C)', color='green')
    ax2.tick_params(axis='y', labelcolor='green')
    ax2.legend(loc='upper right')

    # Aligning the 0°C tick marks
    max_temp = max(max(daily_highs), max(daily_averages))
    min_temp = min(min(daily_lows), min(daily_averages))
    ax1.set_ylim(min_temp - 5, max_temp + 5)
    ax2.set_ylim(min_temp - 5, max_temp + 5)

    # Save the image to memory
    buf = BytesIO()
    plt.savefig(buf, format='png', bbox_inches='tight')
    buf.seek(0)
    image_base64 = base64.b64encode(buf.read()).decode('utf-8')
    plt.close(fig)

    return image_base64

def create_precipitation_chances_pie_charts(precipitation_chances: list, dates: list) -> str:
    
    """
    Create pie charts for precipitation chances and return the corresponding base64 string.

    Args:
    precipitation_chances (List[float]): A list of precipitation chances for each date.
    dates (List[str]): A list of dates corresponding to the precipitation chances.

    Returns:
    str: A base64 encoded string of the image containing the pie charts.
    
    Usage Example:
        >>> create_precipitation_chances_pie_charts([0, 0, 0, 0, 0],
                                                    ['2025-02-18', '2025-02-19', '2025-02-20', '2025-02-21', '2025-02-22'])
        
        It should return a Base64 encoding of a string type (specific example results are not displayed because the image converted to encoding is too long) 
    """
    # Set the size of the figure
    plt.figure(figsize=(15, 5))

    # Plot a pie chart for each date
    for i, (date, chance) in enumerate(zip(dates, precipitation_chances)):
        ax = plt.subplot(1, len(dates), i + 1)
        
        # Draw the pie chart
        wedges, texts = ax.pie(
            [chance, 100 - chance],
            colors=['#66ccff', 'white'],
            startangle=90,
            radius=0.5,
            wedgeprops=dict(edgecolor='darkblue', linewidth=2)
        )
        
        # Remove axis labels
        ax.set_yticklabels([])
        ax.set_xticklabels([])
        
        # Add text annotation for the precipitation chance
        ax.text(0.5, 0, f"{chance:.2f}%", transform=ax.transAxes, ha='center', va='center', fontsize=35,
                fontweight='bold', fontstyle='italic', color='#9370DB')
        
        # Add text annotation for the date
        ax.text(0.5, -0.3, date, transform=ax.transAxes, ha='center', va='center', fontsize=25,
                fontweight='bold', fontstyle='italic', color='#6A5ACD')

    # Adjust the spacing between subplots
    plt.tight_layout()

    # Save the figure to a BytesIO object
    buffer = BytesIO()
    plt.savefig(buffer, format='png', bbox_inches='tight', pad_inches=0.2)
    plt.close()
    
    # Return the base64 encoded image string
    return base64.b64encode(buffer.getvalue()).decode()


def create_weather_forecast_table(weather_icons: list, weather_conditions: list, dates: list) -> str:
    """
    Creates a weather forecast table with icons and descriptions for the next five days and returns a base64 encoded image string.

    Args:
    weather_icons (List[str]): List of OpenWeatherMap icon codes for the weather.
    weather_conditions (List[str]): List of weather conditions descriptions.
    dates (List[str]): List of dates for the forecast.

    Returns:
    str: Base64 encoded image string of the weather forecast table.
    
    Usage Example:
        >>> create_weather_forecast_table(['04d', '04d', '04d', '04d', '04d'],
                                          ['overcast clouds', 'overcast clouds', 'overcast clouds', 'overcast clouds', 'overcast clouds'], 
                                          ['2025-02-18', '2025-02-19', '2025-02-20', '2025-02-21', '2025-02-22'])  
        
        It should return a Base64 encoding of a string type (specific example results are not displayed because the image converted to encoding is too long) 
    """

    # Create the plot
    fig, axs = plt.subplots(3, 5, figsize=(15, 6), gridspec_kw={'height_ratios': [0.5, 0.3, 0.2]})

    # Populate the plot
    for i in range(5):
        # Fetch and display the weather icon
        icon = get_weather_icon(weather_icons[i])
        resized_icon = icon.resize((80, 80))  # Resize the icon
        axs[0, i].imshow(resized_icon, aspect='equal')
        axs[0, i].axis('off')

        # Add weather condition description
        axs[1, i].text(0.5, 0.05, weather_conditions[i], ha='center', va='center', fontsize=22,
                       fontweight='bold', color='#9370DB')
        axs[1, i].axis('off')

        # Add date
        axs[2, i].text(0.5, 0.15, dates[i], ha='center', va='center', fontsize=19,
                       fontweight='bold', fontstyle='italic', color='#6A5ACD')
        axs[2, i].axis('off')

    plt.tight_layout()

    # Save the figure to a BytesIO object
    buffer = BytesIO()
    plt.savefig(buffer, format='png', bbox_inches='tight', pad_inches=0.2)
    plt.close()

    # Return the base64 encoded image string
    return base64.b64encode(buffer.getvalue()).decode()
