from fastapi import APIRouter
from pydantic import BaseModel
import datetime as dt
import src.forecast.bodyParameters.locations as loc
import src.forecast.bodyParameters.forecast_type as type
import src.forecast.bodyParameters.variables as var

router = APIRouter()

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
        "temperature": ["25.5", "26.3", "26.1", "26.0", "26.3", "25.5", "26.3", "26.1", "26.0", "26.3", "25.5", "26.3", "26.1", "26.0", "26.3", "25.5", "26.3", "26.1", "26.0", "26.3", "25.5", "26.3", "26.1"],
        "humidity": ["80.1", "77.8", "77.8", "77.7", "83.0", "80.1", "77.8", "77.8", "77.7", "83.0", "80.1", "77.8", "77.8", "77.7", "83.0", "80.1", "77.8", "77.8", "80.1", "77.8", "77.8", "77.7", "83.0"],
        "precipitation": ["0.0", "0.9", "1.0", "0.5", "0.8", "0.0", "0.9", "1.0", "0.5", "0.8", "0.0", "0.9", "1.0", "0.5", "0.8", "0.0", "0.9", "1.0", "0.5", "0.8", "0.0", "0.9", "1.0"],
        "wind": ["10.0", "12.0", "5.0", "10.0", "12.0", "5.0", "10.0", "12.0", "5.0", "10.0", "12.0", "5.0", "10.0", "12.0", "5.0", "10.0", "12.0", "5.0", "10.0", "12.0", "5.0", "10.0", "3.0"],
        "pressure": ["900", "800", "700", "900", "800", "700", "900", "800", "700", "900", "800", "700", "900", "800", "700", "900", "800", "700", "900", "800", "700", "900", "800"],
        "visibility": ["10000", "12000", "13000", "10000", "12000", "13000", "10000", "12000", "13000", "10000", "12000", "13000", "10000", "12000", "13000", "10000", "12000", "13000", "10000", "12000", "13000", "10000", "15000"],
        "cloud": ["25", "29", "16", "25", "29", "16", "25", "29", "16", "25", "29", "16", "25", "29", "16", "25", "29", "16", "25", "29", "16", "25", "29"],
        "condition": ["Sunny", "Sunny", "Cloudy", "Sunny", "Sunny", "Cloudy", "Sunny", "Sunny", "Cloudy", "Sunny", "Sunny", "Cloudy", "Sunny", "Sunny", "Cloudy", "Sunny", "Sunny", "Cloudy", "Sunny", "Sunny", "Cloudy", "Sunny", "Light Rain"],
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
    
    return {
        "datetime": filterHourlyForecast()
    }
    return res

"""
Filters hourly forecasts to only return data points after current hour until 23:00.
"""
def filterHourlyForecast():
    current_hour = dt.datetime.now().hour
    hours_left_in_day = 23 - current_hour
    res = {}
    for hour in range(hours_left_in_day + 1):
        hour += current_hour
        res[hour] = "test"
    return res