from fastapi import APIRouter
from pydantic import BaseModel
import src.forecast.bodyParameters.locations as loc
import src.forecast.bodyParameters.forecast_type as type
import src.forecast.bodyParameters.variables as var

# For weather forecasting model inference
from keras.models import load_model
import joblib

router = APIRouter()

"""
Get a list of valid locations. This includes cities and towns.

Returns:
    {
        string: {
            "lat": double
            "float": double
        }
    }   
"""
@router.get("/locations")
async def getLocations():
    res = loc.Locations().getLocations()
    return res

"""
Get a list of valid forecast durations.

Returns:
    {
        "locations": list[str]
    }
"""
@router.get("/forecastTypes")
async def getForecastTypes():
    res = {
        "forecastTypes": type.ForecastType().getTypes()
    }
    return res

"""
Get a list of valid weather variables.

Returns:
    {
        "locations": list[str]
    }
"""
@router.get("/variables")
async def getVariables():
    res = {
        "variables": var.Variables().getVariables()
    }
    return res

class forecastBody(BaseModel):
    location: str
    forecastType: str
    variables: list[str]
    
"""
Get the forecast of a location.

Arguments:
    {
        "location": str
        "forecastType": str
        "variables": list[str]
    }

Returns:
    {
        "success": bool,
        "temperature": (optional) list[float],
        "humidity": (optional) list[float],
        "precipitation": (optional) list[float],
    } 
"""    
@router.post("/forecast")
async def getForecast(body: forecastBody):
    res = {
        "success": False
    }
    
    # Check if request body is valid
    isValidLocation = body.location in loc.Locations().getLocations()
    isValidForecastType = body.forecastType in type.ForecastType().getTypes()
    isValidVariables = all(item in var.Variables().getVariables() for item in body.variables)
    
    # TODO: Hardcoded variables returned for now, replace with models
    # TODO: Filter hourly results to only return forecasts after current time
    mock_res = {
        "temperature": ["25.5", "26.3", "26.1", "26.0", "26.3"],
        "humidity": ["80.1", "77.8", "77.8", "77.7", "83.0"],
        "precipitation": ["0.0", "0.9", "1.0", "0.5", "0.8"]
    }
    
    # Invalid request body
    if (not isValidLocation \
        or not isValidForecastType \
        or not isValidVariables):
        return res
    
    # Return requested variables
    for v in body.variables:
        res[v] = mock_res[v]
    res["success"] = True
    
    return res

   
"""
Get the houlry and daily forecast of a location in one api call. Return of api call is fixed.

Arguments:
    {
        "location": str
    }

Returns:
    {
        "success": bool,
        "hourly": {
            "time": list[str],
            "temperature": list[float],
            "pressure": list[float],
            "humidity": list[float],
            "precipitation": list[float],
            "wind_speed": list[float],
            "wind_direction": list[float],
            "cloud_cover": list[float],
        },

        "daily": {
            "time": list[str],
            "temperature": list[float],
            "pressure": list[float],
            "humidity": list[float],
            "precipitation": list[float],
            "wind_speed": list[float],
            "wind_direction": list[float],
            "cloud_cover": list[float],
        }
    } 
"""    
@router.post("/weather-forecast")
async def getForecast(body: forecastBody):
    res = {
        "success": False
    }
    
    location_code = body.location
    
    # Check if request body is valid
    isValidLocation = location_code in loc.Locations().getLocations()
    

    # Invalid request body
    if (not isValidLocation):
        return res
    
    # # TODO: Filter hourly results to only return forecasts after current time
    # mock_res = {
    #     "temperature": ["25.5", "26.3", "26.1", "26.0", "26.3"],
    #     "humidity": ["80.1", "77.8", "77.8", "77.7", "83.0"],
    #     "precipitation": ["0.0", "0.9", "1.0", "0.5", "0.8"]
    # }
    
    # Use valid location to load saved forecast model according 
    model_location = f'../../models/{location_code}/model.h5'   # Load the model from an HDF5 file
    model = load_model(model_location)

    # Load feature scalier object according to location 
    scaler_location = f'../../../weather-forecasting/models/{location_code}/scaler.pkl'
    scaler = joblib.load(scaler_location)

    # Return requested variables
    # for v in body.variables:
    #     res[v] = mock_res[v]
    res["success"] = True
    
    return res