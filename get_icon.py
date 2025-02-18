# -*- coding: utf-8 -*-
"""
Created on Wed Feb 12 14:45:57 2025

@author: keiii
"""

from typing import Literal
from httpx import get
from PIL import Image
from io import BytesIO

def get_weather_icon(icon_code: Literal["01d", "01n", "02d", "02n", "03d", "03n", "04d", "04n", "09d", "09n", "10d", "10n", "11d", "11n", "13d", "13n", "50d", "50n"]) -> Image:
    """
    Download and return a weather icon image based on the provided OpenWeatherMap icon code.

    Args:
        icon_code (str): A valid OpenWeatherMap icon code. Supported codes include:
            - "01d": Clear sky day
            - "01n": Clear sky night
            - "02d": Few clouds day
            - "02n": Few clouds night
            - "03d": Scattered clouds day
            - "03n": Scattered clouds night
            - "04d": Broken clouds day
            - "04n": Broken clouds night
            - "09d": Shower rain day
            - "09n": Shower rain night
            - "10d": Rain day
            - "10n": Rain night
            - "11d": Thunderstorm day
            - "11n": Thunderstorm night
            - "13d": Snow day
            - "13n": Snow night
            - "50d": Mist day
            - "50n": Mist night

    Returns:
        Image: A PIL Image object representing the weather icon.
            Example response:
            <PIL.PngImagePlugin.PngImageFile image mode=RGBA size=50x50 at 0x1E944F24BF0>
    
    Usage Example:
        >>> get_weather_icon('01d')
        <PIL.PngImagePlugin.PngImageFile image mode=RGBA size=50x50 at 0x1E944F24BF0>
    """

    OPENWEATHERMAP_ICON_URL = "http://openweathermap.org/img/wn/{icon}.png"
    response = get(OPENWEATHERMAP_ICON_URL.format(icon=icon_code))
    response.raise_for_status()  # Ensure the request was successful
    return Image.open(BytesIO(response.content))
