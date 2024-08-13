from fastapi import FastAPI, File, UploadFile
from pydantic import BaseModel
import parameters.locations as loc
import parameters.forecast_type as type

app = FastAPI()

class forecastBody(BaseModel):
    location: str
    forecastType: str

@app.get("/locations")
async def getLocations():
    return loc.Locations().getLocations()

@app.get("/forecastTypes")
async def getForecastTypes():
    return type.ForecastType().getTypes()

@app.get("/forecast")
async def getForecast(body: forecastBody):
    if (body.location in loc.Locations().getLocations() \
        and body.forecastType in type.ForecastType().getTypes()):
        return {"success": True}
    return {"success": False, "reason": "Invalid location or forecastType provided."}