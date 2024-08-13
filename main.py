from fastapi import FastAPI, File, UploadFile
from pydantic import BaseModel
from typing import List
import parameters.locations as loc
import parameters.forecast_type as type
import parameters.variables as var

app = FastAPI()

class forecastBody(BaseModel):
    location: str
    forecastType: str
    variables: list[str]

@app.get("/locations")
async def getLocations():
    res = {
        "locations": loc.Locations().getLocations()
    }
    return res

@app.get("/forecastTypes")
async def getForecastTypes():
    res = {
        "forecastTypes": type.ForecastType().getTypes()
    }
    return res

@app.get("/variables")
async def getVariables():
    res = {
        "variables": var.Variables().getVariables()
    }
    return res

@app.get("/forecast")
async def getForecast(body: forecastBody):
    res = {
        "success": False
    }
    
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
    
    if (not isValidLocation \
        or not isValidForecastType \
        or not isValidVariables):
        return res
    
    for v in body.variables:
        res[v] = mock_res[v]
    res["success"] = True
    
    return res
        