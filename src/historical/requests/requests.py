from fastapi import APIRouter
from pydantic import BaseModel
import requests
import datetime as dt
import src.forecast.bodyParameters.locations as loc
from .wwo_weather_code import wwo_weather_code as weather_code

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
    
    res = {"success": False}
    
    if isValidLocation:
        # Parameters for API
        parameters = [
            "temperature_2m",
            "relative_humidity_2m",
            "precipitation",
            "pressure_msl",
            "weather_code",
            "cloud_cover",
            "visibility",
            "wind_speed_10m"
        ]
        
        # Get coordinates of location
        coord = loc.Locations().getLocations()[body.location]
        lat, lon = coord["lat"], coord["lon"]
        
        # Historical data from how many days ago
        days_ago = 7

        # Construct URL
        url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&hourly={','.join(parameters)}&past_days={days_ago}&forecast_days=0"
        resApi = requests.get(url)
        
        if resApi.status_code == 200:
            resApi = resApi.json()
            uniqueDates = getUniqueDates(resApi["hourly"]["time"])
   
            # For each day
            for i in range(len(uniqueDates)):
                res[uniqueDates[i]] = {} # Create dictionary for each day
                # For each parameter
                for parameter in parameters:
                    todayData = resApi["hourly"][parameter][i*24:(i*24)+24]
                    # Do not average weather code
                    if (parameter == "weather_code"):
                        res[uniqueDates[i]][parameter] = todayData
                    # Average hourly data
                    else:
                        avg = averageParameter(todayData)
                        res[uniqueDates[i]][parameter] = avg
            
            res["success"] = True
            
            return res

    return res

"""
Returns a list of unique dates from a list of datetime objects

Arguments:
    datetimes: List[datetime]
    
Return:
    dates: List[datetime]
"""
def getUniqueDates(datetimes):
    dates = []
    format = "%Y-%m-%dT%H:%M"
    for date in datetimes:
        date = (dt.datetime.strptime(date, format)).date() # Parse string to datetime
        if (date not in dates):
            dates.append(date)  # Unique date
    return dates

"""
Averages a list of weather parameters

Arguments:
    datetimes: List[int/double]
    
Return:
    dates: double
"""
def averageParameter(parameters):
    return sum(parameters)/len(parameters)

