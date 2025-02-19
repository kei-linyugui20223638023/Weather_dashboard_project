import requests

def get_city_name_auto(coordinates: str) -> str:
    """
    Fetches the city name based on the provided latitude and longitude coordinates.
    
    Args:
        coordinates (str): A string containing the latitude and longitude values, formatted as "lat, lon".
    
    Returns:
        str: The city name in English, with any instances of "City" removed.
        Example response:
        Beijing
        
    Usage Example:
        >>> get_city_name_auto('39.9042, 116.4074')
        Beijing
    """
    
    # Parse the latitude and longitude string
    lat, lon = map(float, coordinates.split(","))
    
    # Use OpenWeatherMap API to get the city name
    api_key="your_api_key_here"  #Replace your API keys here
    url = f"https://api.openweathermap.org/geo/1.0/reverse?lat={lat}&lon={lon}&limit=1&appid={api_key}"
    
    response = requests.get(url)
    data = response.json()
    
    # Extract the city name and remove "City" from it because Chinese city name with "city" like "Guangzhou City" could be found but "Guangzhou" can.
    org_city_name = data[0]["name"]
    city_name = org_city_name.replace('City', '')  # Remove "City" from the city name
    
    return city_name
