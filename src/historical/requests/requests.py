from fastapi import APIRouter
from pydantic import BaseModel
import requests
import datetime as dt
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
        
        parameters = [
            "temperature_2m",
            "relative_humidity_2m",
            # "precipitation",
            # "weather_code",
            # "cloud_cover",
            # "visibility",
            # "wind_speed_10m"
        ]

        # Parameters
        url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&hourly={','.join(parameters)}&past_days=2&forecast_days=0"

        res = requests.get(url)
        if res.status_code == 200:
            res = res.json()
            uniqueDates = getUniqueDates(res["hourly"]["time"])
            
            new = {}    
            for i in range(len(uniqueDates)):
                new[uniqueDates[i]] = {}
                for parameter in parameters:   
                    today = res["hourly"][parameter][i*24:(i*24)+24]
                    avg = averageDay(today)
                    # print(len(today), today)
                    new[uniqueDates[i]][parameter] = avg
            
            return new
            return res

    return {"success": False}

def getUniqueDates(datetimes):
    dates = []
    format = "%Y-%m-%dT%H:%M"
    for date in datetimes:
        date = (dt.datetime.strptime(date, format)).date()
        if (date not in dates):
            dates.append(date)
    return dates

def averageDay(variables):
    return sum(variables)/len(variables)

