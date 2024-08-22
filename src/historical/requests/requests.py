from fastapi import APIRouter
from pydantic import BaseModel
import requests
import src.forecast.bodyParameters.locations as loc

router = APIRouter()

class historicalBody(BaseModel):
    location: str   # as defined in locations.py
    
"""
Gets the historical weather variables from one location.

Arguments:
    {
        "location": string (as defined in locations.py or GET /locations endpoint)
    }
    
Return:
"""    
@router.post("/historical")
async def getCurrentWeather(body: historicalBody):
    
    isValidLocation = body.location in loc.Locations().getLocations()
    
    if isValidLocation:
        # Get coordinates of location
        coord = loc.Locations().getLocations()[body.location]
        lat, lon = coord["lat"], coord["lon"]
        
        # Parameters
        url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&hourly=temperature_2m,relative_humidity_2m,apparent_temperature,precipitation,weather_code,cloud_cover,visibility,wind_speed_10m,wind_speed_80m,wind_speed_120m,wind_speed_180m,temperature_80m,temperature_120m,temperature_180m&past_days=7&forecast_days=1"

        res = requests.get(url)
        if res.status_code == 200:
            res = res.json()    
            return res
    
    return {"success": False}

