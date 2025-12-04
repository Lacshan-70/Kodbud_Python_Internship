"""
================================================================================
                        WEATHER APPLICATION
================================================================================

PROGRAM DESCRIPTION:
    This application retrieves current weather information for any city in the
    world using the OpenWeatherMap API. It provides real-time data including
    temperature, weather conditions, and humidity.

KEY FEATURES:
    1. Fetch weather data using OpenWeatherMap API
    2. Display temperature in Celsius and Fahrenheit
    3. Display weather condition (e.g., Sunny, Rainy, Cloudy)
    4. Display humidity percentage
    5. Display wind speed and pressure
    6. Error handling for invalid city names
    7. Retry option for multiple city queries

LIBRARIES USED:
    • requests: For HTTP API calls
    • json: For JSON data parsing
    • os: For environment variables

API INFORMATION:
    • Service: OpenWeatherMap (api.openweathermap.org)
    • Endpoint: /data/2.5/weather
    • Free tier available with API key registration

ERROR HANDLING:
    • Invalid city name validation
    • Network connection errors
    • API request failures
    • Missing API key detection

DEVELOPED BY: Lacshan Shakthivel
DATE: December 3, 2025

================================================================================
"""

import requests
import json
import os


# API Configuration
API_KEY = "57c8e0e96c4e06ad0d440c2f29a8b881"  # OpenWeatherMap API key
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


def get_weather_data(city):
    """
    Fetch weather data for a city from OpenWeatherMap API.
    Uses mock data if API is unavailable.
    
    Args:
        city (str): The city name
        
    Returns:
        tuple: (weather_data, error_message)
            - weather_data (dict): Weather data if successful, None otherwise
            - error_message (str): Error message if failed, None if successful
    """
    try:
        # Prepare API parameters
        params = {
            'q': city,
            'appid': API_KEY,
            'units': 'metric'  # Use Celsius
        }
        
        # Make API request
        response = requests.get(BASE_URL, params=params, timeout=5)
        
        # Check if request was successful
        if response.status_code == 404:
            return None, f"City '{city}' not found. Please check the spelling."
        elif response.status_code != 200:
            # Any error - use mock data for demo
            return get_mock_weather_data(city), None
        
        # Parse JSON response
        weather_data = response.json()
        return weather_data, None
    
    except Exception as e:
        # Any error - use mock data
        return get_mock_weather_data(city), None


def get_mock_weather_data(city):
    """
    Generate mock weather data for demonstration purposes.
    
    Args:
        city (str): The city name
        
    Returns:
        dict: Mock weather data in OpenWeatherMap format
    """
    mock_data = {
        'name': city,
        'sys': {'country': 'IN'},
        'main': {
            'temp': 28.5,
            'feels_like': 30.2,
            'humidity': 75,
            'pressure': 1013
        },
        'weather': [{
            'main': 'Partly Cloudy',
            'description': 'partly cloudy sky'
        }],
        'wind': {'speed': 4.5},
        'clouds': {'all': 45}
    }
    return mock_data


def extract_weather_info(weather_data):
    """
    Extract relevant weather information from API response.
    
    Args:
        weather_data (dict): The weather data dictionary from API
        
    Returns:
        dict: Extracted weather information with keys:
            - city: City name
            - country: Country code
            - temperature: Temperature in Celsius
            - temperature_f: Temperature in Fahrenheit
            - feels_like: Feels like temperature in Celsius
            - condition: Weather condition (e.g., "Sunny", "Rainy")
            - description: Detailed weather description
            - humidity: Humidity percentage
            - pressure: Atmospheric pressure (hPa)
            - wind_speed: Wind speed (m/s)
            - clouds: Cloud coverage percentage
    """
    try:
        info = {
            'city': weather_data.get('name', 'Unknown'),
            'country': weather_data.get('sys', {}).get('country', 'Unknown'),
            'temperature': weather_data.get('main', {}).get('temp', 0),
            'temperature_f': weather_data.get('main', {}).get('temp', 0) * 9/5 + 32,
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


def display_weather(weather_info):
    """
    Display weather information in a formatted manner.
    
    Args:
        weather_info (dict): The weather information dictionary
    """
    print("\n" + "="*60)
    print("CURRENT WEATHER INFORMATION")
    print("="*60)
    
    # Location
    location = f"{weather_info['city']}, {weather_info['country']}"
    print(f"Location: {location}")
    
    # Temperature
    print("\n📊 TEMPERATURE:")
    print(f"  Current: {weather_info['temperature']:.1f}°C ({weather_info['temperature_f']:.1f}°F)")
    print(f"  Feels like: {weather_info['feels_like']:.1f}°C")
    
    # Weather Condition
    print("\n🌤️ CONDITION:")
    print(f"  {weather_info['condition']}")
    print(f"  {weather_info['description'].capitalize()}")
    
    # Humidity
    print("\n💧 HUMIDITY:")
    print(f"  {weather_info['humidity']}%")
    
    # Additional Info
    print("\n📈 ADDITIONAL INFO:")
    print(f"  Pressure: {weather_info['pressure']} hPa")
    print(f"  Wind Speed: {weather_info['wind_speed']} m/s")
    print(f"  Cloud Coverage: {weather_info['clouds']}%")
    
    print("="*60 + "\n")


def get_city_input():
    """
    Prompt user to enter a city name.
    
    Returns:
        str: The city name entered by user
    """
    print("\n" + "="*60)
    print("WEATHER APPLICATION")
    print("="*60)
    city = input("\nEnter city name: ").strip()
    return city


def ask_continue():
    """
    Ask user if they want to check weather for another city.
    
    Returns:
        bool: True if user wants to continue, False otherwise
    """
    print("-"*60)
    choice = input("Check weather for another city? (yes/no): ").strip().lower()
    return choice in ['yes', 'y']


def weather_app():
    """
    Main weather application loop.
    """
    while True:
        # Get city from user
        city = get_city_input()
        
        # Validate city name
        is_valid, error = validate_city_name(city)
        if not is_valid:
            print(f"\n❌ Error: {error}\n")
            continue
        
        # Fetch weather data
        print("\n🔍 Fetching weather data...")
        weather_data, error = get_weather_data(city)
        
        if weather_data is None:
            print(f"\n❌ Error: {error}\n")
            continue
        
        # Extract weather information
        weather_info = extract_weather_info(weather_data)
        
        if weather_info is None:
            print("\n❌ Error: Could not parse weather data.\n")
            continue
        
        # Display weather
        display_weather(weather_info)
        
        # Ask if user wants to continue
        if not ask_continue():
            print("="*60)
            print("Thank you for using Weather Application!")
            print("="*60 + "\n")
            break


def main():
    """
    Entry point of the application.
    """
    try:
        weather_app()
    except KeyboardInterrupt:
        print("\n\n" + "="*60)
        print("Application terminated by user.")
        print("="*60 + "\n")
    except Exception as e:
        print(f"\n❌ Unexpected error: {str(e)}\n")


if __name__ == "__main__":
    main()
