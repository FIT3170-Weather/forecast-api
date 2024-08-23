from retry_requests import retry
import openmeteo_requests
import requests_cache
import src.forecast.bodyParameters.locations as loc
from datetime import datetime

def getLastYearWeatherData(location_code, days=3):
    # Setup the Open-Meteo API client with cache and retry on error
    cache_session = requests_cache.CachedSession('.cache', expire_after = -1)
    retry_session = retry(cache_session, retries = 5, backoff_factor = 0.2)
    openmeteo = openmeteo_requests.Client(session = retry_session)

    locations = loc.Locations().getLocations()
    location = locations[location_code]

    # Get previous year first day date and last day date 

    # Get today's date
    today = datetime.now()

    # Calculate the first day and last day of the previous year
    first_day_of_previous_year = datetime(today.year - 1, 1, 1)
    last_day_of_previous_year = datetime(today.year - 1, 12, 31)

    # Get the past 3 days of hourly weather data
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": location["lat"],
        "longitude": location["lon"],
        "start_date": first_day_of_previous_year,
        "end_date": last_day_of_previous_year,
        "daily": ["temperature_2m_mean", "precipitation_sum"]
    }

    try:
        responses = openmeteo.weather_api(url, params=params)
        response = populateFromResponse(responses[0])
    except:
        return
    
    return response