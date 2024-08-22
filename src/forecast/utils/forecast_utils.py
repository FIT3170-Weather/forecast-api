import os
import openmeteo_requests

import requests_cache
from retry_requests import retry
import pandas as pd
import src.forecast.bodyParameters.locations as loc
import numpy as np


# For weather forecasting model inference
from keras.models import load_model
import joblib


PREDICTED_ATTRIBUTES = ['temperature_2m', 'relative_humidity_2m', 'dew_point_2m', 'rain', 'pressure_msl', 'wind_speed_10m', 'wind_direction_10m']


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
    # convert dataframe to numpy array
    input = dataframe.to_numpy()

    # Use valid location to load saved forecast model according 
    model_location = f'../weather-forecasting/models/{location_code}/model.h5'   # Load the model from an HDF5 file
    model = load_model(model_location)

    # Load feature scalier object according to location 
    scaler_location = f'../weather-forecasting/models/{location_code}/scaler.pkl'
    scaler = joblib.load(scaler_location)

    # Scale the input values for prediction
    scaled_input = scaler.transform(input)
    
    # Must predict hours_to_forecast hours into the future by performing auto-regression
    forecast = np.empty((0, 7))

    for i in range(hours_to_forecast):
        scaled_input = scaled_input.reshape(1, 72, 7)

        # Perform prediction
        prediction = model.predict(scaled_input)
        forecast = np.vstack([forecast, prediction])

        scaled_input = scaled_input.reshape(72, 7)

        # Update dataframe with new prediction
        scaled_input = np.vstack([scaled_input, prediction])
        scaled_input = scaled_input[1:, :] # Remove the first row

    # Inverse transform the forecasted values
    forecast = scaler.inverse_transform(forecast)
    
    return forecast



"""
Prepare the forecast results as a JSON response

"hourly_units": {
    "time": "iso8601",
    "temperature_2m": "°C",
    "relative_humidity_2m": "%",
    "dew_point_2m": "°C",
    "rain": "mm",
    "pressure_msl": "hPa",
    "wind_speed_10m": "km/h",
    "wind_direction_10m": "°"
}
"""
def prepareForecastJSON(forecast_dataframe, total_hours_to_forecast, day_hours_to_predict, result_dict):
    
    # Get each row as a list
    forecast_results = forecast_dataframe.values.tolist()

    temperature = forecast_dataframe[PREDICTED_ATTRIBUTES[0]].values.tolist()
    humidity = forecast_dataframe[PREDICTED_ATTRIBUTES[1]].values.tolist()

    real_feel = [round(heat_index(temperature[i], humidity[i])) for i in range(total_hours_to_forecast)]
    temperature = [round(temperature[i]) for i in range(len(temperature))]
    humidity = [round(humidity[i]) for i in range(len(humidity))]


    dew_point = [round(i) for i in forecast_dataframe[PREDICTED_ATTRIBUTES[2]].values.tolist()]
    precipitation = [round(i, 1) for i in forecast_dataframe[PREDICTED_ATTRIBUTES[3]].values.tolist()]
    pressure = [round(i) for i in forecast_dataframe[PREDICTED_ATTRIBUTES[4]].values.tolist()]
    wind_speed = [round(i) for i in forecast_dataframe[PREDICTED_ATTRIBUTES[5]].values.tolist()]
    wind_direction = [round(i) for i in forecast_dataframe[PREDICTED_ATTRIBUTES[6]].values.tolist()]
    

    # Stich the forecast results as a JSON response
    result_dict["hourly"] = {
        "time": [],
        "temperature": temperature[:day_hours_to_predict],
        "real_feel": real_feel[:day_hours_to_predict],
        "humidity": humidity[:day_hours_to_predict],
        "precipitation": precipitation[:day_hours_to_predict],
        "pressure": pressure[:day_hours_to_predict],
        "wind_speed": wind_speed[:day_hours_to_predict],
        "wind_direction": wind_direction[:day_hours_to_predict],
        "dew_point": dew_point[:day_hours_to_predict]
    }

    result_dict["daily"] = {
        "time": [],
        "temperature": temperature[:day_hours_to_predict],
        "humidity": humidity[:day_hours_to_predict],
        "dew_point": dew_point[:day_hours_to_predict],
        "precipitation": precipitation[:day_hours_to_predict],
        "pressure": pressure[:day_hours_to_predict],
        "wind_speed": pressure[:day_hours_to_predict],
        "wind_direction": pressure[:day_hours_to_predict],
    }
    
    return result_dict


def heat_index(temperature, humidity):
    """
    Calculate the heat index.
    
    :param temperature: Temperature in degrees Celsius
    :param humidity: Relative humidity as a percentage
    :return: Heat index
    """
    T = temperature
    H = humidity
    
    # Coefficients for the heat index formula
    c1 = -8.78469475556
    c2 = 1.61139411
    c3 = 2.33854883889
    c4 = -0.14611605
    c5 = -0.012308094
    c6 = -0.0164248277778
    c7 = 0.002211732
    c8 = 0.00072546
    c9 = -0.000003582

    heat_index_value = (c1 + c2*T + c3*H + c4*T*H + c5*T**2 +
                        c6*H**2 + c7*T**2*H + c8*T*H**2 + c9*T**2*H**2)
    return heat_index_value

def wind_chill_index(temperature, wind_speed):
    """
    Calculate the wind chill index.
    
    :param temperature: Temperature in degrees Celsius
    :param wind_speed: Wind speed in km/h
    :return: Wind chill index
    """
    return (13.12 + 0.6215 * temperature - 11.37 * wind_speed**0.16 +
            0.3965 * temperature * wind_speed**0.16)

def degrees_to_direction(degrees):
    """
    Convert wind direction from degrees to compass direction, handling degrees beyond 360.
    
    :param degrees: Wind direction in degrees (can be greater than 360)
    :return: Compass direction as a string
    """
    # Wrap degrees to be within [0, 360)
    degrees = degrees % 360

    # Define the ranges for each compass direction
    if (337.5 <= degrees < 360) or (0 <= degrees < 22.5):
        return 'N'
    elif 22.5 <= degrees < 45:
        return 'NE'
    elif 45 <= degrees < 67.5:
        return 'ENE'
    elif 67.5 <= degrees < 90:
        return 'E'
    elif 90 <= degrees < 112.5:
        return 'ESE'
    elif 112.5 <= degrees < 135:
        return 'SE'
    elif 135 <= degrees < 157.5:
        return 'SSE'
    elif 157.5 <= degrees < 180:
        return 'S'
    elif 180 <= degrees < 202.5:
        return 'SSW'
    elif 202.5 <= degrees < 225:
        return 'SW'
    elif 225 <= degrees < 247.5:
        return 'WSW'
    elif 247.5 <= degrees < 270:
        return 'W'
    elif 270 <= degrees < 292.5:
        return 'WNW'
    elif 292.5 <= degrees < 315:
        return 'NW'
    elif 315 <= degrees < 337.5:
        return 'NNW'