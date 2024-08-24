from fastapi import APIRouter
import datetime as dt
import src.forecast.bodyParameters.locations as loc
from src.statistical.utils.statistical_utils import getLastYearWeatherData

router = APIRouter()

"""
Gets the Monthly statistical data for precipitation and temperature. Size of information is 12 months. 
First item in list is January and last item is December.

Arguments:
    Query_param:
        location_code: string (as defined in locations.py or GET /locations endpoint)
    
Return:
    {
        "success": bool
        "temperature": [int],
        "total_precipitation": [int],
        "precipitation_days": [int]
    }
"""    
@router.get("/monthly")
async def getMonthlyWeatherStatisics(location_code: str):
    isValidLocation = location_code in loc.Locations().getLocations()
    
    res = {
        "success": False
    }

    if not isValidLocation:
        return res
    
    # Get the last year weather data as a dataframe
    year_df = getLastYearWeatherData(location_code)
    year_df['precipitation_days'] = (year_df['precipitation_sum'] > 1).astype(int)

    # Group date by month and then average the mean temperatuer of each day and add the monthly precipitation total
    # add count for total sum > 1mm of precipitation, Less than 1mm of precipitation is considered as no precipitation
    monthly_df = year_df.resample("ME").agg({
        "temperature_2m_mean": "mean",
        "precipitation_sum": "sum",
        "precipitation_days": "sum"
    })

    res["months"] = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
    res["temperature"] = monthly_df["temperature_2m_mean"].round().astype(int).tolist()
    res["total_precipitation"] = monthly_df["precipitation_sum"].round().astype(int).tolist()
    res["precipitation_days"] = monthly_df["precipitation_days"].tolist()
    res["success"] = True

    return res
