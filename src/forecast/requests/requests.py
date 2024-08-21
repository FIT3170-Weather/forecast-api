from fastapi import APIRouter
from pydantic import BaseModel
from src.forecast.utils.forecast_utils import getPreviousHourlyData
import src.forecast.bodyParameters.locations as loc
import src.forecast.bodyParameters.forecast_type as type
import src.forecast.bodyParameters.variables as var

from datetime import datetime
import pytz


router = APIRouter()

FORECAST_PREV_DAYS = 3 # Past 3 days for inference
FORECAST_CURRENT_DAYS = 1 # This means the current day also used in inference
DAYS_TO_FORECAST = 7
PREDICTED_ATTRIBUTES = ['temperature_2m', 'relative_humidity_2m', 'dew_point_2m', 'rain', 'pressure_msl', 'wind_speed_10m', 'wind_direction_10m']
TIMEZONE = 'Asia/Singapore'

"""
Get a list of valid locations. This includes cities and towns.

Returns:
    {
        string: {
            "lat": double
            "float": double
        }
    }   
"""
@router.get("/locations")
async def getLocations():
    res = loc.Locations().getLocations()
    return res

"""
Get a list of valid forecast durations.

Returns:
    {
        "locations": list[str]
    }
"""
@router.get("/forecastTypes")
async def getForecastTypes():
    res = {
        "forecastTypes": type.ForecastType().getTypes()
    }
    return res

"""
Get a list of valid weather variables.

Returns:
    {
        "locations": list[str]
    }
"""
@router.get("/variables")
async def getVariables():
    res = {
        "variables": var.Variables().getVariables()
    }
    return res

class forecastBody(BaseModel):
    location: str
    forecastType: str
    variables: list[str]
    
"""
Get the forecast of a location.

Arguments:
    {
        "location": str
        "forecastType": str
        "variables": list[str]
    }

Returns:
    {
        "success": bool,
        "temperature": (optional) list[float],
        "humidity": (optional) list[float],
        "precipitation": (optional) list[float],
    } 
"""    
@router.post("/forecast")
async def getForecast(body: forecastBody):
    res = {
        "success": False
    }
    
    # Check if request body is valid
    isValidLocation = body.location in loc.Locations().getLocations()
    isValidForecastType = body.forecastType in type.ForecastType().getTypes()
    isValidVariables = all(item in var.Variables().getVariables() for item in body.variables)
    
    # TODO: Hardcoded variables returned for now, replace with models
    # TODO: Filter hourly results to only return forecasts after current time
    mock_res = {
        "temperature": ["25.5", "26.3", "26.1", "26.0", "26.3"],
        "humidity": ["80.1", "77.8", "77.8", "77.7", "83.0"],
        "precipitation": ["0.0", "0.9", "1.0", "0.5", "0.8"]
    }
    
    # Invalid request body
    if (not isValidLocation \
        or not isValidForecastType \
        or not isValidVariables):
        return res
    
    # Return requested variables
    for v in body.variables:
        res[v] = mock_res[v]
    res["success"] = True
    
    return res

   
"""
Get the houlry and daily forecast of a location in one api call. Return of api call is fixed.

Arguments:
    {
        "location": str
    }

Returns:
    {
        "success": bool,
        "hourly": {
            "time": list[str],
            "temperature": list[float],
            "pressure": list[float],
            "humidity": list[float],
            "precipitation": list[float],
            "wind_speed": list[float],
            "wind_direction": list[float],
            "cloud_cover": list[float],
        },

        "daily": {
            "time": list[str],
            "temperature": list[float],
            "pressure": list[float],
            "humidity": list[float],
            "precipitation": list[float],
            "wind_speed": list[float],
            "wind_direction": list[float],
            "cloud_cover": list[float],
        }
    } 
"""    
@router.get("/weather-forecast")
async def getWeatherForecast(location_code: str):
    res = {
        "success": False
    }

    # Check if request body is valid
    isValidLocation = location_code in loc.Locations().getLocations()
    
    # Invalid request body
    if (not isValidLocation):
        return res

    # Get the data for past 3 days (72 hours) of hourly weather data
    hourly_dataframe = getPreviousHourlyData(location_code, days=FORECAST_PREV_DAYS) # Dataframe should have 72 + 24 = 96 rows (72 for 3 past dat days and 24 for the current day)

    # calculate how many hours left in the current day according to current timezone
    current_hour = datetime.now(pytz.timezone(TIMEZONE)).hour
    day_hours_to_predict = 24 - current_hour # Hours left to predict for the current day
    total_hours_to_forecast = day_hours_to_predict + DAYS_TO_FORECAST*24 # Total hours to forecast for the current day and the next 7 days
    
    # get the final 72 hours of data for prediction from the hourly dataframe based on the current hour
    hourly_dataframe = hourly_dataframe.iloc[current_hour:FORECAST_PREV_DAYS*24 + current_hour]

    # check if number of rows is 72
    if hourly_dataframe.shape[0] != FORECAST_PREV_DAYS*24:
        return res

    # Make the forecast

    # Stich the forecast results as a JSON response

    # Return requested variables
    # for v in body.variables:
    #     res[v] = mock_res[v]
    res["success"] = True
    
    return res