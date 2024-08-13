from fastapi import FastAPI
from pydantic import BaseModel
import bodyParameters.locations as loc
import bodyParameters.forecast_type as type
import bodyParameters.variables as var

app = FastAPI() # "uvicorn main:app" to run on localhost:8000

"""
Get a list of valid locations. This includes cities and towns.

Returns:
    {
        "locations": list[str]
    }
"""
@app.get("/locations")
async def getLocations():
    res = {
        "locations": loc.Locations().getLocations()
    }
    return res

"""
Get a list of valid forecast durations.

Returns:
    {
        "locations": list[str]
    }
"""
@app.get("/forecastTypes")
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
@app.get("/variables")
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
@app.get("/forecast")
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
        