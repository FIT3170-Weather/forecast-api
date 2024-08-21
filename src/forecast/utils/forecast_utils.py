import openmeteo_requests

import requests_cache
from retry_requests import retry
import pandas as pd
import src.forecast.bodyParameters.locations as loc
import numpy as np

# For weather forecasting model inference
from keras.models import load_model
import joblib

# Function to get the previous houly data
def getPreviousHourlyData(location_code, days=3):
    # Setup the Open-Meteo API client with cache and retry on error
    cache_session = requests_cache.CachedSession('.cache', expire_after = -1)
    retry_session = retry(cache_session, retries = 5, backoff_factor = 0.2)
    openmeteo = openmeteo_requests.Client(session = retry_session)

    locations = loc.Locations().getLocations()
    location = locations[location_code]

    # Get the past 3 days of hourly weather data
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": location["lat"],
        "longitude": location["lon"],
        "hourly": ["temperature_2m", "relative_humidity_2m", "dew_point_2m", "rain", "pressure_msl", "wind_speed_10m", "wind_direction_10m"],
        "timezone": "Asia/Singapore",
        "past_days": days,
        "forecast_days": 1
    }

    try:
        responses = openmeteo.weather_api(url, params=params)
        response = populateFromResponse(responses[0])
    except:
        return
    
    return response

# Stiches the openmeteo response into a dataframe, this dataframe will be used in inference
def populateFromResponse(response):
    # Process hourly data. The order of variables needs to be the same as requested.
    hourly = response.Hourly()
    hourly_temperature_2m = hourly.Variables(0).ValuesAsNumpy()
    hourly_relative_humidity_2m = hourly.Variables(1).ValuesAsNumpy()
    hourly_dew_point_2m = hourly.Variables(2).ValuesAsNumpy()
    hourly_rain = hourly.Variables(3).ValuesAsNumpy()
    hourly_pressure_msl = hourly.Variables(4).ValuesAsNumpy()
    hourly_wind_speed_10m = hourly.Variables(5).ValuesAsNumpy()
    hourly_wind_direction_10m = hourly.Variables(6).ValuesAsNumpy()

    hourly_data = {"date": pd.date_range(
        start = pd.to_datetime(hourly.Time(), unit = "s", utc = True),
        end = pd.to_datetime(hourly.TimeEnd(), unit = "s", utc = True),
        freq = pd.Timedelta(seconds = hourly.Interval()),
        inclusive = "left"
    )}

    hourly_data["temperature_2m"] = hourly_temperature_2m
    hourly_data["relative_humidity_2m"] = hourly_relative_humidity_2m
    hourly_data["dew_point_2m"] = hourly_dew_point_2m
    hourly_data["rain"] = hourly_rain
    hourly_data["pressure_msl"] = hourly_pressure_msl
    hourly_data["wind_speed_10m"] = hourly_wind_speed_10m
    hourly_data["wind_direction_10m"] = hourly_wind_direction_10m

    hourly_dataframe = pd.DataFrame(data = hourly_data)
    hourly_dataframe.set_index("date", inplace = True)

    return hourly_dataframe


def makeForecast(dataframe, location_code, hours_to_forecast):
    # convert dataframe to numpy arrayn
    input = dataframe.to_numpy()

    # Use valid location to load saved forecast model according 
    model_location = f'../../models/{location_code}/model.h5'   # Load the model from an HDF5 file
    model = load_model(model_location)

    # Load feature scalier object according to location 
    scaler_location = f'../../../weather-forecasting/models/{location_code}/scaler.pkl'
    scaler = joblib.load(scaler_location)

    # Must predict hours_to_forecast hours into the future by performing auto-regression
    forecast = []
    for i in range(hours_to_forecast):
        # Scale the input
        input_scaled = scaler.transform(input)

        # Perform prediction
        prediction = model.predict(input_scaled)
        forecast.append(scaler.inverse_transform(prediction))

        # Update dataframe with new prediction
        dataframe = np.append(dataframe, prediction)
        dataframe = np.delete(dataframe, 0)
    pass