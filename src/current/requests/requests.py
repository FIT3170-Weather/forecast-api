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

"""
Gets the current weather variables from all fixed locations.

Arguments:
    None
    
Return:
    {
        "success": bool,
        "location_code": [string],
        "temperature": [int],
        "weather_main": [string],
        "weather_desc": [string]
    }
"""    
@router.get("/all-locations-current")
async def getCurrentWeather():
    locations = loc.Locations().getLocations()

    location_codes = []
    temperatures = []
    weather_mains = []
    weather_descs = []

    for location in locations:
        coord = locations[location]
        lat, lon = coord["lat"], coord["lon"]
        url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={API_KEY}&units=metric"
        response = requests.get(url)
        if response.status_code != 200:
            return {"success": False} 
        else:
            response = response.json()
            location_codes.append(location)
            temperatures.append(int(response["main"]["temp"]))
            weather_mains.append(response["weather"][0]["main"])
            weather_descs.append(response["weather"][0]["description"])

    res = {
        "success": True,
        "location_code": location_codes,
        "temperature": temperatures,
        "weather_main": weather_mains,
        "weather_desc": weather_descs
    }
    
    return res