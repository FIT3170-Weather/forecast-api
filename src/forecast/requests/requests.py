from fastapi import APIRouter
from pydantic import BaseModel
<<<<<<< HEAD
import datetime as dt
=======
from forecast.utils.forecast_utils import getPreviousHourlyData
>>>>>>> 14f3cc90787386583f8746e703eab74c5d53422c
import src.forecast.bodyParameters.locations as loc
import src.forecast.bodyParameters.forecast_type as type
import src.forecast.bodyParameters.variables as var

from datetime import datetime
import pytz

# For weather forecasting model inference
from keras.models import load_model
import joblib

router = APIRouter()

<<<<<<< HEAD
# TODO: Hardcoded variables returned for now, replace with models
# TODO: Filter hourly results to only return forecasts after current time
mock_res_hourly = {
    "temperature": ["25.5", "26.3", "26.1", "26.0", "26.3", "25.5", "26.3", "26.1", "26.0", "26.3", "25.5", "26.3", "26.1", "26.0", "26.3", "25.5", "26.3", "26.1", "26.0", "26.3", "25.5", "26.3", "26.1"],
    "humidity": ["80.1", "77.8", "77.8", "77.7", "83.0", "80.1", "77.8", "77.8", "77.7", "83.0", "80.1", "77.8", "77.8", "77.7", "83.0", "80.1", "77.8", "77.8", "80.1", "77.8", "77.8", "77.7", "83.0"],
    "precipitation": ["0.0", "0.9", "1.0", "0.5", "0.8", "0.0", "0.9", "1.0", "0.5", "0.8", "0.0", "0.9", "1.0", "0.5", "0.8", "0.0", "0.9", "1.0", "0.5", "0.8", "0.0", "0.9", "1.0"],
    "wind": ["10.0", "12.0", "5.0", "10.0", "12.0", "5.0", "10.0", "12.0", "5.0", "10.0", "12.0", "5.0", "10.0", "12.0", "5.0", "10.0", "12.0", "5.0", "10.0", "12.0", "5.0", "10.0", "3.0"],
    "pressure": ["900", "800", "700", "900", "800", "700", "900", "800", "700", "900", "800", "700", "900", "800", "700", "900", "800", "700", "900", "800", "700", "900", "800"],
    "visibility": ["10000", "12000", "13000", "10000", "12000", "13000", "10000", "12000", "13000", "10000", "12000", "13000", "10000", "12000", "13000", "10000", "12000", "13000", "10000", "12000", "13000", "10000", "15000"],
    "cloud": ["25", "29", "16", "25", "29", "16", "25", "29", "16", "25", "29", "16", "25", "29", "16", "25", "29", "16", "25", "29", "16", "25", "29"],
    "condition": ["Sunny", "Sunny", "Cloudy", "Sunny", "Sunny", "Cloudy", "Sunny", "Sunny", "Cloudy", "Sunny", "Sunny", "Cloudy", "Sunny", "Sunny", "Cloudy", "Sunny", "Sunny", "Cloudy", "Sunny", "Sunny", "Cloudy", "Sunny", "Light Rain"],
}
mock_res_daily = {
    "temperature": ["25.5", "26.3", "26.1", "26.0", "26.3", "25.5", "26.3"],
    "humidity": ["80.1", "77.8", "77.8", "77.7", "83.0", "80.1", "77.8"],
    "precipitation": ["0.0", "0.9", "1.0", "0.5", "0.8", "0.0", "0.9"],
    "wind": ["10.0", "12.0", "5.0", "10.0", "12.0", "5.0", "10.0"],
    "pressure": ["900", "800", "700", "900", "800", "700", "900"],
    "visibility": ["10000", "12000", "13000", "10000", "12000", "13000", "10000"],
    "cloud": ["25", "29", "16", "25", "29", "16", "25"],
    "condition": ["Sunny", "Sunny", "Cloudy", "Sunny", "Sunny", "Cloudy", "Sunny"],
}
=======
FORECAST_PREV_DAYS = 3 # Past 3 days for inference
FORECAST_CURRENT_DAYS = 1 # This means the current day also used in inference
DAYS_TO_FORECAST = 7
TIMEZONE = 'Asia/Singapore'
>>>>>>> 14f3cc90787386583f8746e703eab74c5d53422c

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
        "success": False,
        "forecast": {},
    }
    
    # Check if request body is valid
    isValidLocation = body.location in loc.Locations().getLocations()
    isValidForecastType = body.forecastType in type.ForecastType().getTypes()
    isValidVariables = all(item in var.Variables().getVariables() for item in body.variables)
    
    # Invalid request body
    if (not isValidLocation \
        or not isValidForecastType \
        or not isValidVariables):
        return res
    
    # Return requested variables
    # Hourly
    if (body.forecastType == "hourly"):
        hours = getRemainingHours() # Hours left in day until 23:00
        data = mock_res_hourly
        
        # Data for remaining hours
        for v in body.variables:
            data[v] = data[v][-len(hours):]
        
        # Each hour forecast
        for i in range(len(hours)):
            res["forecast"][hours[i]] = {}
            # Each variable
            for v in body.variables:
                res["forecast"][hours[i]][v] = data[v][i]    
        res["success"] = True
        
        return res
    
    # Daily
    # TODO: Wait and see how model returns data before changing
    for v in body.variables:
        res["forecast"][v] = mock_res_daily[v]
    res["success"] = True
    
    return res

<<<<<<< HEAD
"""
Determine hours from (CURRENT HOUR + 1) until 23:00.

Used to prevent request from returning forecast for past time.
"""
def getRemainingHours():
    current_datetime = dt.datetime.now()
    current_hour = current_datetime.hour
    hours_left_in_day = 23 - current_hour
    
    res = []
    for hour in range(1, hours_left_in_day + 1):
        hour += current_hour # To actual datetime hours left in day
        res.append(dt.datetime(
            year=current_datetime.year, 
            month=current_datetime.month, 
            day=current_datetime.day,
            hour=hour,
            minute=0,
            second=0,
            ))

=======
   
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
@router.post("/weather-forecast")
async def getForecast(body: forecastBody):
    res = {
        "success": False
    }

    #TODO: Change to query parameters
    
    location_code = body.location
    
    # Check if request body is valid
    isValidLocation = location_code in loc.Locations().getLocations()
    
    # Invalid request body
    if (not isValidLocation):
        return res
    
    # Use valid location to load saved forecast model according 
    model_location = f'../../models/{location_code}/model.h5'   # Load the model from an HDF5 file
    model = load_model(model_location)

    # Load feature scalier object according to location 
    scaler_location = f'../../../weather-forecasting/models/{location_code}/scaler.pkl'
    scaler = joblib.load(scaler_location)

    # Get the data for past 3 days (72 hours) of hourly weather data
    hourly_dataframe = getPreviousHourlyData(location_code, days=FORECAST_PREV_DAYS) # Dataframe should have 72 + 24 = 96 rows (72 for 3 past dat days and 24 for the current day)

    # calculate how many hours left in the current day according to current timezone
    current_hour = datetime.datetime.now(pytz.timezone(TIMEZONE)).hour
    day_hours_to_predict = 24 - current_hour # Hours left to predict for the current day
    total_hours_to_forecast = day_hours_to_predict + DAYS_TO_FORECAST*24 # Total hours to forecast for the current day and the next 7 days
    
    # get the final 72 hours of data for prediction from the hourly dataframe based on the current hour
    hourly_dataframe = hourly_dataframe.iloc[current_hour:FORECAST_PREV_DAYS*24 + current_hour]

    # check if number of rows is 72
    if hourly_dataframe.shape[0] != FORECAST_PREV_DAYS*24:
        return res

    # convert to numpy array and make prediction

    # Format the hourly data received to get the last 72 hours preceeding the current hour

    # Use the model to predict the next remaining hours of the day and the next 7 days of data (auto regressively)

    # Return requested variables
    # for v in body.variables:
    #     res[v] = mock_res[v]
    res["success"] = True
    
>>>>>>> 14f3cc90787386583f8746e703eab74c5d53422c
    return res