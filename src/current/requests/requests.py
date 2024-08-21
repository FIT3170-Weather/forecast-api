from fastapi import APIRouter
from pydantic import BaseModel
import requests
import src.forecast.bodyParameters.locations as loc
from .apiKey import API_KEY

router = APIRouter()

class currentBody(BaseModel):
    location: str   # as defined in locations.py

"""
Gets the current weather variables from one location.

Arguments:
    {
        "location": string (as defined in locations.py or GET /locations endpoint)
    }
    
Return:
    See: https://openweathermap.org/current#example_JSON
"""    
@router.post("/current")
async def getCurrentWeather(body: currentBody):
    
    isValidLocation = body.location in loc.Locations().getLocations()
    
    if isValidLocation:
        # Get coordinates of location
        coord = loc.Locations().getLocations()[body.location]
        lat, lon = coord["lat"], coord["lon"]
        url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={API_KEY}&units=metric"
        
        res = requests.get(url)
        if res.status_code == 200:
            res = res.json()
            
            # Get Subang coordinates
            subang_coords = loc.Locations().getLocations()["subang-jaya"]
            subang_lat, subang_lon = subang_coords["lat"], subang_coords["lon"]
            
            # If response coordinates == Subang coordinates
            if (res["coord"]["lat"] == subang_lat and res["coord"]["lon"] == subang_lon):
                # Change name to Subang Jaya (API incorrectly sets it as 'Petaling')
                res["name"] = "Subang Jaya"
                
            return res
    
    return {"success": False}