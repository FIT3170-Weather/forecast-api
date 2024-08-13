from fastapi import FastAPI, File, UploadFile
from pydantic import BaseModel
import parameters.locations as loc
import parameters.forecast_type as type
import parameters.variables as var

app = FastAPI()

class forecastBody(BaseModel):
    location: str
    forecastType: str

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
    if (body.location in loc.Locations().getLocations() \
        and body.forecastType in type.ForecastType().getTypes()):
        return {"success": True}
    return {"success": False, "reason": "Invalid location or forecastType provided."}