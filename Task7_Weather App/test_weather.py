"""
================================================================================
                        WEATHER APPLICATION - TEST CASES
================================================================================

TEST SUITE DESCRIPTION:
    This test module validates all functionalities of the Weather Application
    including city validation, API data retrieval, and weather information
    parsing.

TEST COVERAGE:
    1. City name validation
    2. Weather data retrieval from API
    3. Weather information extraction
    4. Temperature conversion
    5. API key validation
    6. Response validation
    7. Humidity level descriptions
    8. Weather condition emojis

DEVELOPED BY: Lacshan Shakthivel
DATE: December 3, 2025

================================================================================
"""

import unittest
import sys
import os
from unittest.mock import patch, MagicMock

# Get the directory of the current script and add it to path
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)

from weather_logic import (
    validate_city_name, get_weather_data, extract_weather_info,
    celsius_to_fahrenheit, validate_api_key, validate_response,
    get_humidity_level, get_weather_emoji
)


class TestValidateCityName(unittest.TestCase):
    """
    Test cases for the validate_city_name() function.
    """
    
    def test_valid_city_name_single_word(self):
        """Test valid single-word city name"""
        is_valid, error = validate_city_name("London")
        self.assertTrue(is_valid)
        self.assertIsNone(error)
    
    def test_valid_city_name_two_words(self):
        """Test valid multi-word city name"""
        is_valid, error = validate_city_name("New York")
        self.assertTrue(is_valid)
        self.assertIsNone(error)
    
    def test_valid_city_name_with_hyphen(self):
        """Test valid city name with hyphen"""
        is_valid, error = validate_city_name("Los-Angeles")
        self.assertTrue(is_valid)
        self.assertIsNone(error)
    
    def test_valid_city_name_lowercase(self):
        """Test valid lowercase city name"""
        is_valid, error = validate_city_name("paris")
        self.assertTrue(is_valid)
        self.assertIsNone(error)
    
    def test_invalid_city_name_empty(self):
        """Test invalid empty city name"""
        is_valid, error = validate_city_name("")
        self.assertFalse(is_valid)
        self.assertIn("empty", error.lower())
    
    def test_invalid_city_name_whitespace(self):
        """Test invalid whitespace-only city name"""
        is_valid, error = validate_city_name("   ")
        self.assertFalse(is_valid)
        self.assertIn("empty", error.lower())
    
    def test_invalid_city_name_single_char(self):
        """Test invalid single character city name"""
        is_valid, error = validate_city_name("A")
        self.assertFalse(is_valid)
        self.assertIn("at least 2", error)
    
    def test_invalid_city_name_numbers(self):
        """Test invalid city name with numbers"""
        is_valid, error = validate_city_name("City123")
        self.assertFalse(is_valid)
        self.assertIn("letters", error.lower())
    
    def test_invalid_city_name_special_chars(self):
        """Test invalid city name with special characters"""
        is_valid, error = validate_city_name("City@#$")
        self.assertFalse(is_valid)
        self.assertIn("letters", error.lower())
    
    def test_valid_city_name_with_spaces_trimmed(self):
        """Test city name with leading/trailing spaces"""
        is_valid, error = validate_city_name("  Tokyo  ")
        self.assertTrue(is_valid)
        self.assertIsNone(error)


class TestGetWeatherData(unittest.TestCase):
    """
    Test cases for the get_weather_data() function.
    """
    
    @patch('weather_logic.requests.get')
    def test_valid_weather_data_retrieval(self, mock_get):
        """Test successful weather data retrieval"""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            'name': 'London',
            'main': {'temp': 15},
            'weather': [{'main': 'Cloudy'}]
        }
        mock_get.return_value = mock_response
        
        data, error = get_weather_data("London")
        
        self.assertIsNotNone(data)
        self.assertIsNone(error)
        self.assertEqual(data['name'], 'London')
    
    @patch('weather_logic.requests.get')
    def test_city_not_found(self, mock_get):
        """Test 404 error for non-existent city"""
        mock_response = MagicMock()
        mock_response.status_code = 404
        mock_get.return_value = mock_response
        
        data, error = get_weather_data("NonExistentCity")
        
        self.assertIsNone(data)
        self.assertIn("not found", error)
    
    @patch('weather_logic.requests.get')
    def test_invalid_api_key(self, mock_get):
        """Test 401 error for invalid API key"""
        mock_response = MagicMock()
        mock_response.status_code = 401
        mock_get.return_value = mock_response
        
        data, error = get_weather_data("London")
        
        self.assertIsNone(data)
        self.assertIn("Invalid API key", error)
    
    @patch('weather_logic.requests.get')
    def test_rate_limit_exceeded(self, mock_get):
        """Test 429 error for rate limit"""
        mock_response = MagicMock()
        mock_response.status_code = 429
        mock_get.return_value = mock_response
        
        data, error = get_weather_data("London")
        
        self.assertIsNone(data)
        self.assertIn("rate limit", error.lower())
    
    @patch('weather_logic.requests.get')
    def test_connection_error(self, mock_get):
        """Test connection error handling"""
        import requests
        mock_get.side_effect = requests.exceptions.ConnectionError("Connection failed")
        
        data, error = get_weather_data("London")
        
        self.assertIsNone(data)
        self.assertIn("Connection error", error)
    
    @patch('weather_logic.requests.get')
    def test_timeout_error(self, mock_get):
        """Test timeout error handling"""
        import requests
        mock_get.side_effect = requests.exceptions.Timeout("Request timeout")
        
        data, error = get_weather_data("London")
        
        self.assertIsNone(data)
        self.assertIn("timeout", error.lower())


class TestExtractWeatherInfo(unittest.TestCase):
    """
    Test cases for the extract_weather_info() function.
    """
    
    def test_extract_valid_weather_info(self):
        """Test extraction of valid weather data"""
        weather_data = {
            'name': 'London',
            'sys': {'country': 'GB'},
            'main': {'temp': 15, 'feels_like': 12, 'humidity': 70, 'pressure': 1010},
            'weather': [{'main': 'Cloudy', 'description': 'overcast clouds'}],
            'wind': {'speed': 5},
            'clouds': {'all': 75}
        }
        
        info = extract_weather_info(weather_data)
        
        self.assertEqual(info['city'], 'London')
        self.assertEqual(info['country'], 'GB')
        self.assertEqual(info['temperature'], 15)
        self.assertEqual(info['humidity'], 70)
        self.assertEqual(info['condition'], 'Cloudy')
    
    def test_extract_missing_fields(self):
        """Test extraction with missing optional fields"""
        weather_data = {
            'name': 'Tokyo',
            'main': {'temp': 20},
            'weather': [{'main': 'Clear'}]
        }
        
        info = extract_weather_info(weather_data)
        
        self.assertEqual(info['city'], 'Tokyo')
        self.assertEqual(info['temperature'], 20)
    
    def test_extract_empty_dict(self):
        """Test extraction with empty dictionary"""
        info = extract_weather_info({})
        
        self.assertIsNotNone(info)
        self.assertEqual(info['city'], 'Unknown')


class TestCelsiusToFahrenheit(unittest.TestCase):
    """
    Test cases for the celsius_to_fahrenheit() function.
    """
    
    def test_conversion_freezing_point(self):
        """Test conversion at freezing point"""
        result = celsius_to_fahrenheit(0)
        self.assertEqual(result, 32)
    
    def test_conversion_boiling_point(self):
        """Test conversion at boiling point"""
        result = celsius_to_fahrenheit(100)
        self.assertEqual(result, 212)
    
    def test_conversion_room_temperature(self):
        """Test conversion at room temperature"""
        result = celsius_to_fahrenheit(20)
        self.assertAlmostEqual(result, 68, places=1)
    
    def test_conversion_negative_temp(self):
        """Test conversion with negative temperature"""
        result = celsius_to_fahrenheit(-10)
        self.assertEqual(result, 14)
    
    def test_conversion_none(self):
        """Test conversion with None value"""
        result = celsius_to_fahrenheit(None)
        self.assertIsNone(result)


class TestValidateApiKey(unittest.TestCase):
    """
    Test cases for the validate_api_key() function.
    """
    
    def test_valid_api_key(self):
        """Test valid API key"""
        valid_key = "6bfe026e6f84aa5af94ebcc99999e4b6"
        result = validate_api_key(valid_key)
        self.assertTrue(result)
    
    def test_invalid_api_key_too_short(self):
        """Test too short API key"""
        result = validate_api_key("short")
        self.assertFalse(result)
    
    def test_invalid_api_key_none(self):
        """Test None API key"""
        result = validate_api_key(None)
        self.assertFalse(result)
    
    def test_invalid_api_key_empty(self):
        """Test empty API key"""
        result = validate_api_key("")
        self.assertFalse(result)


class TestValidateResponse(unittest.TestCase):
    """
    Test cases for the validate_response() function.
    """
    
    def test_valid_response(self):
        """Test valid API response"""
        response = {
            'name': 'London',
            'main': {'temp': 15},
            'weather': [{'main': 'Cloudy'}],
            'wind': {'speed': 5}
        }
        result = validate_response(response)
        self.assertTrue(result)
    
    def test_invalid_response_missing_field(self):
        """Test response missing required field"""
        response = {
            'name': 'London',
            'main': {'temp': 15}
            # Missing 'weather' and 'wind'
        }
        result = validate_response(response)
        self.assertFalse(result)
    
    def test_invalid_response_not_dict(self):
        """Test non-dictionary response"""
        result = validate_response("not a dict")
        self.assertFalse(result)
    
    def test_invalid_response_none(self):
        """Test None response"""
        result = validate_response(None)
        self.assertFalse(result)


class TestGetHumidityLevel(unittest.TestCase):
    """
    Test cases for the get_humidity_level() function.
    """
    
    def test_humidity_dry(self):
        """Test dry humidity level"""
        level = get_humidity_level(20)
        self.assertEqual(level, "Dry")
    
    def test_humidity_comfortable(self):
        """Test comfortable humidity level"""
        level = get_humidity_level(40)
        self.assertEqual(level, "Comfortable")
    
    def test_humidity_humid(self):
        """Test humid humidity level"""
        level = get_humidity_level(60)
        self.assertEqual(level, "Humid")
    
    def test_humidity_very_humid(self):
        """Test very humid humidity level"""
        level = get_humidity_level(80)
        self.assertEqual(level, "Very Humid")
    
    def test_humidity_boundary_30(self):
        """Test humidity boundary at 30%"""
        level = get_humidity_level(30)
        self.assertEqual(level, "Comfortable")
    
    def test_humidity_boundary_50(self):
        """Test humidity boundary at 50%"""
        level = get_humidity_level(50)
        self.assertEqual(level, "Humid")


class TestGetWeatherEmoji(unittest.TestCase):
    """
    Test cases for the get_weather_emoji() function.
    """
    
    def test_emoji_clear(self):
        """Test emoji for clear weather"""
        emoji = get_weather_emoji("Clear")
        self.assertEqual(emoji, '☀️')
    
    def test_emoji_clouds(self):
        """Test emoji for cloudy weather"""
        emoji = get_weather_emoji("Clouds")
        self.assertEqual(emoji, '☁️')
    
    def test_emoji_rain(self):
        """Test emoji for rainy weather"""
        emoji = get_weather_emoji("Rain")
        self.assertEqual(emoji, '🌧️')
    
    def test_emoji_snow(self):
        """Test emoji for snow"""
        emoji = get_weather_emoji("Snow")
        self.assertEqual(emoji, '❄️')
    
    def test_emoji_thunderstorm(self):
        """Test emoji for thunderstorm"""
        emoji = get_weather_emoji("Thunderstorm")
        self.assertEqual(emoji, '⛈️')
    
    def test_emoji_unknown(self):
        """Test emoji for unknown weather"""
        emoji = get_weather_emoji("Unknown")
        self.assertEqual(emoji, '🌐')
    
    def test_emoji_case_insensitive(self):
        """Test emoji is case-insensitive"""
        emoji_upper = get_weather_emoji("CLEAR")
        emoji_lower = get_weather_emoji("clear")
        self.assertEqual(emoji_upper, emoji_lower)


class TestIntegration(unittest.TestCase):
    """
    Integration tests for weather application workflow.
    """
    
    def test_city_validation_workflow(self):
        """Test city validation workflow"""
        # Valid city
        is_valid, error = validate_city_name("Paris")
        self.assertTrue(is_valid)
        self.assertIsNone(error)
        
        # Invalid city
        is_valid, error = validate_city_name("")
        self.assertFalse(is_valid)
        self.assertIsNotNone(error)
    
    def test_weather_info_extraction_workflow(self):
        """Test complete weather info extraction workflow"""
        weather_data = {
            'name': 'Tokyo',
            'sys': {'country': 'JP'},
            'main': {'temp': 22, 'feels_like': 21, 'humidity': 65, 'pressure': 1013},
            'weather': [{'main': 'Sunny', 'description': 'clear sky'}],
            'wind': {'speed': 3},
            'clouds': {'all': 10}
        }
        
        info = extract_weather_info(weather_data)
        
        # Verify all info extracted correctly
        self.assertEqual(info['city'], 'Tokyo')
        self.assertEqual(info['country'], 'JP')
        self.assertEqual(info['humidity'], 65)
        
        # Test temperature conversion
        fahrenheit = celsius_to_fahrenheit(info['temperature'])
        self.assertAlmostEqual(fahrenheit, 71.6, places=1)
        
        # Test humidity level
        humidity_level = get_humidity_level(info['humidity'])
        self.assertEqual(humidity_level, "Humid")
        
        # Test weather emoji
        emoji = get_weather_emoji(info['condition'])
        self.assertEqual(emoji, '☀️')


def run_test_summary():
    """
    Run all tests and display a summary report.
    """
    print("\n" + "="*80)
    print("RUNNING WEATHER APPLICATION TEST SUITE")
    print("="*80 + "\n")
    
    # Create a test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Add all test classes
    suite.addTests(loader.loadTestsFromTestCase(TestValidateCityName))
    suite.addTests(loader.loadTestsFromTestCase(TestGetWeatherData))
    suite.addTests(loader.loadTestsFromTestCase(TestExtractWeatherInfo))
    suite.addTests(loader.loadTestsFromTestCase(TestCelsiusToFahrenheit))
    suite.addTests(loader.loadTestsFromTestCase(TestValidateApiKey))
    suite.addTests(loader.loadTestsFromTestCase(TestValidateResponse))
    suite.addTests(loader.loadTestsFromTestCase(TestGetHumidityLevel))
    suite.addTests(loader.loadTestsFromTestCase(TestGetWeatherEmoji))
    suite.addTests(loader.loadTestsFromTestCase(TestIntegration))
    
    # Run tests with verbose output
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Print summary
    print("\n" + "="*80)
    print("TEST SUMMARY")
    print("="*80)
    print(f"Tests Run: {result.testsRun}")
    print(f"Successes: {result.testsRun - len(result.failures) - len(result.errors)}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    print("="*80 + "\n")
    
    return result.wasSuccessful()


if __name__ == '__main__':
    success = run_test_summary()
    sys.exit(0 if success else 1)
