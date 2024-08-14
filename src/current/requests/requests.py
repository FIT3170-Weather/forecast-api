# from main import app
from fastapi import APIRouter
from pydantic import BaseModel
import requests
import src.forecast.bodyParameters.locations as loc
from .apiKey import API_KEY

router = APIRouter()

class currentBody(BaseModel):
    location: str
    
@router.get("/current")
async def getCurrentWeather(body: currentBody):
    
    isValidLocation = body.location in loc.Locations().getLocations()
    
    if isValidLocation:
        lat, lon = 3.1319, 101.6841
        url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={API_KEY}"
        
        res = requests.get(url)
        if res.status_code == 200:
            return res.json()
    
    return {"success": False}