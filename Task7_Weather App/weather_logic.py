"""
================================================================================
                        WEATHER APPLICATION - LOGIC MODULE
================================================================================

This module contains the core logic functions for the Weather Application,
separated from the main UI loop for better testability and modularity.

FUNCTIONS:
    1. validate_city_name() - Validate city name input
    2. get_weather_data() - Fetch data from OpenWeatherMap API
    3. extract_weather_info() - Parse API response
    4. celsius_to_fahrenheit() - Temperature conversion
    5. validate_api_key() - Check API key validity
    6. validate_response() - Validate API response format

DEVELOPED BY: Lacshan Shakthivel
DATE: December 3, 2025

================================================================================
"""

import requests
import json


API_KEY = "6bfe026e6f84aa5af94ebcc99999e4b6"
BASE_URL = "https://api.openweathermap.org/data/2.5/weather"


def validate_city_name(city):
    """
    Validate if the city name is not empty and is properly formatted.
    
    Args:
        city (str): The city name to validate
        
    Returns:
        tuple: (is_valid, error_message)
            - is_valid (bool): True if valid, False otherwise
            - error_message (str): Error message if invalid, None if valid
    """
    if not city or not city.strip():
        return False, "City name cannot be empty."
    
    city = city.strip()
    
    # Check minimum length
    if len(city) < 2:
        return False, "City name must be at least 2 characters long."
    
    # Check for valid characters (letters, spaces, hyphens)
    if not all(char.isalpha() or char.isspace() or char == '-' for char in city):
        return False, "City name can only contain letters, spaces, and hyphens."
    
    return True, None


def get_weather_data(city, api_key=API_KEY):
    """
    Fetch weather data for a city from OpenWeatherMap API.
    
    Args:
        city (str): The city name
        api_key (str): OpenWeatherMap API key (default: API_KEY)
        
    Returns:
        tuple: (weather_data, error_message)
            - weather_data (dict): Weather data if successful, None otherwise
            - error_message (str): Error message if failed, None if successful
    """
    try:
        # Prepare API parameters
        params = {
            'q': city,
            'appid': api_key,
            'units': 'metric'  # Use Celsius
        }
        
        # Make API request
        response = requests.get(BASE_URL, params=params, timeout=5)
        
        # Check if request was successful
        if response.status_code == 404:
            return None, f"City '{city}' not found. Please check the spelling."
        elif response.status_code == 401:
            return None, "Invalid API key. Please check your API credentials."
        elif response.status_code == 429:
            return None, "API rate limit exceeded. Please wait a moment."
        elif response.status_code != 200:
            return None, f"API error (Code {response.status_code}). Please try again."
        
        # Parse JSON response
        weather_data = response.json()
        return weather_data, None
    
    except requests.exceptions.ConnectionError:
        return None, "Connection error: Unable to reach the API. Check your internet connection."
    except requests.exceptions.Timeout:
        return None, "Request timeout: The API server is not responding."
    except requests.exceptions.RequestException as e:
        return None, f"Request error: {str(e)}"
    except json.JSONDecodeError:
        return None, "Error parsing API response."
    except Exception as e:
        return None, f"Unexpected error: {str(e)}"


def extract_weather_info(weather_data):
    """
    Extract relevant weather information from API response.
    
    Args:
        weather_data (dict): The weather data dictionary from API
        
    Returns:
        dict: Extracted weather information, or None if parsing failed
    """
    try:
        info = {
            'city': weather_data.get('name', 'Unknown'),
            'country': weather_data.get('sys', {}).get('country', 'Unknown'),
            'temperature': weather_data.get('main', {}).get('temp', 0),
            'feels_like': weather_data.get('main', {}).get('feels_like', 0),
            'condition': weather_data.get('weather', [{}])[0].get('main', 'Unknown'),
            'description': weather_data.get('weather', [{}])[0].get('description', 'Unknown'),
            'humidity': weather_data.get('main', {}).get('humidity', 0),
            'pressure': weather_data.get('main', {}).get('pressure', 0),
            'wind_speed': weather_data.get('wind', {}).get('speed', 0),
            'clouds': weather_data.get('clouds', {}).get('all', 0)
        }
        return info
    except Exception as e:
        return None


def celsius_to_fahrenheit(celsius):
    """
    Convert temperature from Celsius to Fahrenheit.
    
    Args:
        celsius (float): Temperature in Celsius
        
    Returns:
        float: Temperature in Fahrenheit
    """
    if celsius is None:
        return None
    return celsius * 9/5 + 32


def validate_api_key(api_key):
    """
    Validate if the API key is properly formatted.
    
    Args:
        api_key (str): The API key to validate
        
    Returns:
        bool: True if key appears valid, False otherwise
    """
    if not api_key or not isinstance(api_key, str):
        return False
    
    # OpenWeatherMap API keys are typically 32 character hex strings
    if len(api_key) < 20:
        return False
    
    return True


def validate_response(response_data):
    """
    Validate if the API response contains required fields.
    
    Args:
        response_data (dict): The API response data
        
    Returns:
        bool: True if response is valid, False otherwise
    """
    if not isinstance(response_data, dict):
        return False
    
    # Check for required fields
    required_fields = ['name', 'main', 'weather', 'wind']
    
    for field in required_fields:
        if field not in response_data:
            return False
    
    return True


def get_humidity_level(humidity):
    """
    Get humidity level description based on percentage.
    
    Args:
        humidity (int): Humidity percentage (0-100)
        
    Returns:
        str: Humidity level description
    """
    if humidity < 30:
        return "Dry"
    elif humidity < 50:
        return "Comfortable"
    elif humidity < 70:
        return "Humid"
    else:
        return "Very Humid"


def get_weather_emoji(condition):
    """
    Get emoji representing weather condition.
    
    Args:
        condition (str): Weather condition name
        
    Returns:
        str: Emoji representing the condition
    """
    condition_lower = condition.lower()
    
    emoji_map = {
        'clear': '☀️',
        'sunny': '☀️',
        'clouds': '☁️',
        'cloudy': '☁️',
        'rain': '🌧️',
        'rainy': '🌧️',
        'snow': '❄️',
        'snowy': '❄️',
        'mist': '🌫️',
        'fog': '🌫️',
        'thunderstorm': '⛈️',
        'drizzle': '🌦️',
        'hail': '❄️',
    }
    
    for key, emoji in emoji_map.items():
        if key in condition_lower:
            return emoji
    
    return '🌐'  # Default emoji
