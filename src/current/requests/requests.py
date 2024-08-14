# from main import app
from fastapi import APIRouter
from pydantic import BaseModel
import src.forecast.bodyParameters.locations as loc
# from apiKey import API_KEY

router = APIRouter()

class currentBody(BaseModel):
    location: str
    
@router.get("/current")
async def getCurrentWeather(body: currentBody):
    
    isValidLocation = body.location in loc.Locations().getLocations()
    
    if isValidLocation:
        return {"success": True}
    
    return {"success": False}