from fastapi import FastAPI
from pydantic import BaseModel
import src.forecast.bodyParameters.locations as loc
# from apiKey import API_KEY
from .current.requests import requests as current
from .forecast.requests import requests as forecast

app = FastAPI() # "uvicorn main:app --reload" to run on localhost:8000

app.include_router(current.router)
app.include_router(forecast.router)

# class currentBody(BaseModel):
#     location: str
    
# @app.get("/current")
# async def getCurrentWeather(body: currentBody):
    
#     isValidLocation = body.location in loc.Locations().getLocations()
    
#     if isValidLocation:
#         return {"success": True}
    
#     return {"success": False}