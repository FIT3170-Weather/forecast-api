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
    {
        "sucess": bool
        "historical": [
            {
                "date": datetime
                "temperature_2m": double,
                "relative_humidity_2m": double,
                "precipitation": double,
                "pressure_msl": double,
                "weather_code": str,
                "cloud_cover": double,
                "visibility": double,
                "wind_speed_10m": double
            }
        ]
    }
"""    
@router.post("/historical")
async def getCurrentWeather(body: historicalBody):
    isValidLocation = body.location in loc.Locations().getLocations()
    
    res = {
        "success": False,
        "historical": []
        }
    
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
                todayAggregate = {
                    "date": uniqueDates[i]
                    }
                res["historical"].append(todayAggregate) # Create dictionary for each day
                # For each parameter
                for parameter in parameters:
                    todayData = resApi["hourly"][parameter][i*24:(i*24)+24]
                    # Do not average weather code; deicde worst weather condition
                    if (parameter == "weather_code"):
                        todayAggregate[parameter] = determineWorstWeatherCondition(todayData)
                    # Average hourly data
                    else:
                        avg = averageParameter(todayData)
                        todayAggregate[parameter] = avg
            
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
   parameters: List[int/double]
    
Return:
    average: double
"""
def averageParameter(parameters):
    return round(sum(parameters)/len(parameters), 2)

"""
Determines the worst weather condition for the day, based on a list of conditions throughout the day.
Based on WWO Weather Codes.
Starts at 0 with clear, then 98 with thunderstorms.

Arguments:
    conditions: List[int]
    
Return:
    worstCondition: str
"""
def determineWorstWeatherCondition(conditions):
    worstWeather = max(conditions) # Get the worst weather condition for today
    return weather_code[f"{worstWeather}"]

