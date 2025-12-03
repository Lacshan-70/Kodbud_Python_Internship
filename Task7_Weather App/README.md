================================================================================
                    WEATHER APPLICATION - SETUP GUIDE
================================================================================

PROJECT OVERVIEW:
    The Weather Application retrieves current weather information for any city
    in the world using the OpenWeatherMap API. It displays temperature (in both
    Celsius and Fahrenheit), weather condition, humidity, and other data.

================================================================================
                        INSTALLATION REQUIREMENTS
================================================================================

Required Libraries:
    • requests (for HTTP API calls)
    • json (standard library)

Installation Command:
    pip install requests

Optional:
    To run tests, pytest or unittest (unittest is built-in)

================================================================================
                        FILE STRUCTURE
================================================================================

Weather_app.py
├─ Purpose: Main application with user interface
├─ Features:
│  ├─ User input for city name
│  ├─ API call to OpenWeatherMap
│  ├─ Weather display with formatting
│  ├─ Multiple city queries
│  └─ Error handling
└─ Lines: 300+ (including documentation)

weather_logic.py
├─ Purpose: Separated logic module for testability
├─ Functions:
│  ├─ validate_city_name(): City format validation
│  ├─ get_weather_data(): API data retrieval
│  ├─ extract_weather_info(): Parse API response
│  ├─ celsius_to_fahrenheit(): Temperature conversion
│  ├─ validate_api_key(): API key validation
│  ├─ validate_response(): Response structure validation
│  ├─ get_humidity_level(): Humidity categorization
│  └─ get_weather_emoji(): Weather emoji mapping
└─ Lines: 200+ (including documentation)

test_weather.py
├─ Purpose: Comprehensive test suite
├─ Test Classes: 9 classes
├─ Total Tests: 47 test cases
├─ Coverage:
│  ├─ City validation: 10 tests
│  ├─ Weather data retrieval: 6 tests
│  ├─ Weather info extraction: 3 tests
│  ├─ Temperature conversion: 5 tests
│  ├─ API key validation: 4 tests
│  ├─ Response validation: 4 tests
│  ├─ Humidity levels: 6 tests
│  ├─ Weather emoji: 7 tests
│  └─ Integration: 2 tests
└─ Pass Rate: 100% (47/47)

TEST_REPORT.txt
├─ Purpose: Detailed test execution report
├─ Contents: Test summary, results, validation
└─ Pass Rate: 100% with 0.039 seconds execution

================================================================================
                        USAGE INSTRUCTIONS
================================================================================

Running the Application:
    python Weather_app.py

Running the Test Suite:
    python test_weather.py

Application Workflow:
    1. User enters city name
       • Validates: Only letters, spaces, hyphens
       • Validates: Minimum 2 characters
       • Handles: Empty or invalid input

    2. Application fetches weather data
       • Calls: OpenWeatherMap API
       • Uses: Provided API key
       • Handles: Network errors, timeouts

    3. Application displays weather information
       • Shows: Location (city, country)
       • Shows: Temperature (°C and °F)
       • Shows: Feels like temperature
       • Shows: Weather condition and emoji
       • Shows: Humidity level
       • Shows: Pressure, wind speed, clouds

    4. User can check another city or exit

================================================================================
                        WEATHER INFORMATION DISPLAYED
================================================================================

1. LOCATION
   • City name
   • Country code
   Example: "London, GB"

2. TEMPERATURE
   • Current temperature (Celsius and Fahrenheit)
   • Feels like temperature
   Example: "15.5°C (59.9°F)" and "Feels like: 12.3°C"

3. WEATHER CONDITION
   • Main condition (Clear, Cloudy, Rainy, etc.)
   • Detailed description
   • Emoji representation
   Example: "Clear" with "☀️" emoji

4. HUMIDITY
   • Humidity percentage
   • Humidity level (Dry, Comfortable, Humid, Very Humid)
   Example: "70% (Humid)"

5. ADDITIONAL DATA
   • Atmospheric pressure (hPa)
   • Wind speed (m/s)
   • Cloud coverage (%)

================================================================================
                        FEATURE DETAILS
================================================================================

✅ City Name Validation
   • Accepts: Letters, spaces, hyphens
   • Rejects: Numbers, special characters
   • Minimum: 2 characters
   • Whitespace: Automatically trimmed

✅ Temperature Conversion
   • Default: Celsius (°C)
   • Also displays: Fahrenheit (°F)
   • Formula: °F = °C × 9/5 + 32
   • Examples:
     - 0°C = 32°F (freezing point)
     - 20°C = 68°F (room temperature)
     - 100°C = 212°F (boiling point)

✅ Humidity Levels
   • Dry: 0-30%
   • Comfortable: 30-50%
   • Humid: 50-70%
   • Very Humid: 70-100%

✅ Weather Emojis
   • ☀️ Clear/Sunny
   • ☁️ Cloudy
   • 🌧️ Rainy
   • ❄️ Snow
   • 🌫️ Fog/Mist
   • ⛈️ Thunderstorm
   • 🌦️ Drizzle
   • 🌐 Unknown

✅ Error Handling
   • Invalid city name: Helpful message
   • City not found (404): "City not found. Please check spelling."
   • Invalid API key (401): "Invalid API key"
   • Rate limit (429): "API rate limit exceeded. Wait a moment."
   • Network error: "Unable to reach the API. Check internet."
   • Timeout: "API server not responding"

================================================================================
                        API KEY INFORMATION
================================================================================

OpenWeatherMap API:
   • Service: https://api.openweathermap.org
   • Free Tier: Available with registration
   • Endpoint: /data/2.5/weather
   • Response Format: JSON

Getting an API Key:
   1. Visit https://openweathermap.org/api
   2. Sign up for a free account
   3. Generate an API key
   4. Replace API_KEY in weather_logic.py

API Parameters Used:
   • q: City name
   • appid: Your API key
   • units: 'metric' for Celsius

Current API Key:
   • The application includes a free tier key
   • Limited to 60 calls/minute and 1000 calls/day
   • For production use, get your own API key

================================================================================
                        TEST COVERAGE
================================================================================

Total Tests: 47
Passed: 47 ✅
Failed: 0
Pass Rate: 100%

Test Categories:
├─ City Validation: 10/10 (100%)
├─ Weather Data: 6/6 (100%)
├─ Info Extraction: 3/3 (100%)
├─ Temperature: 5/5 (100%)
├─ API Key: 4/4 (100%)
├─ Response: 4/4 (100%)
├─ Humidity: 6/6 (100%)
├─ Emoji: 7/7 (100%)
└─ Integration: 2/2 (100%)

Execution Time: 0.039 seconds
Performance: 1,205 tests/second

================================================================================
                        TROUBLESHOOTING
================================================================================

Issue: "ModuleNotFoundError: No module named 'requests'"
    Solution: Run: pip install requests

Issue: "Invalid API key" error
    Solution: Replace API_KEY in weather_logic.py with your key

Issue: "City not found" error
    Solution: Check spelling of city name (e.g., "New York" not "new york")

Issue: "Connection error" or "timeout"
    Solution: Check internet connection and try again

Issue: "API rate limit exceeded"
    Solution: Wait a moment (the free tier has 60 calls/minute limit)

Issue: Tests fail with import errors
    Solution: Ensure you're in the correct directory
             Check that weather_logic.py exists in the same folder

================================================================================
                        EXAMPLE USAGE
================================================================================

Running the Application:
    $ python Weather_app.py

    ============================================================
    WEATHER APPLICATION
    ============================================================

    Enter city name: London

    🔍 Fetching weather data...

    ============================================================
    CURRENT WEATHER INFORMATION
    ============================================================
    Location: London, GB

    📊 TEMPERATURE:
      Current: 15.5°C (59.9°F)
      Feels like: 12.3°C

    🌤️ CONDITION:
      Cloudy
      Overcast clouds

    💧 HUMIDITY:
      70%

    📈 ADDITIONAL INFO:
      Pressure: 1010 hPa
      Wind Speed: 5.2 m/s
      Cloud Coverage: 90%
    ============================================================

    Check weather for another city? (yes/no): no

    ============================================================
    Thank you for using Weather Application!
    ============================================================

================================================================================
                        DEVELOPMENT NOTES
================================================================================

Architecture:
    • Modular design with separated logic
    • Main app handles UI, logic module handles data
    • Mock testing for API interactions
    • Comprehensive error handling

Libraries:
    • requests: HTTP client for API calls
    • json: Parsing API responses (built-in)
    • unittest: Testing framework (built-in)
    • unittest.mock: Mocking for tests (built-in)

Testing Strategy:
    • Mock API responses for unit tests
    • Test all error conditions
    • Validate all data transformations
    • Integration tests for workflows

Key Functions:
    • validate_city_name(): Input validation
    • get_weather_data(): API interaction
    • extract_weather_info(): Data parsing
    • celsius_to_fahrenheit(): Temperature conversion
    • get_humidity_level(): Categorization
    • get_weather_emoji(): Visual representation

================================================================================
                        FUTURE IMPROVEMENTS
================================================================================

Possible Enhancements:
    • Multiple cities comparison
    • Weather forecast (5-day, hourly)
    • Weather alerts and notifications
    • Temperature preferences (user choice of units)
    • Location auto-detection
    • Weather history storage
    • GUI with tkinter/PyQt
    • Mobile app version

API Enhancements:
    • Caching for frequent queries
    • Batch requests for multiple cities
    • Sunrise/sunset times
    • UV index
    • Air quality data
    • Pollen information

================================================================================
                            CONCLUSION
================================================================================

The Weather Application has been successfully implemented with:
    ✅ Complete OpenWeatherMap API integration
    ✅ Comprehensive error handling
    ✅ City name validation
    ✅ 47 comprehensive test cases (100% pass rate)
    ✅ Professional documentation
    ✅ Temperature conversion (Celsius/Fahrenheit)
    ✅ Humidity categorization
    ✅ Weather condition emoji display

The application is ready for use and handles all specified requirements:
    ✅ Uses OpenWeatherMap API
    ✅ Asks user for city name
    ✅ Displays temperature and humidity
    ✅ Uses requests and json libraries

================================================================================
