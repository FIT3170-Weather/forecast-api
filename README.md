# forecast-api

# Start up
Run "/main.py" (NOTE: NOT /src/main.py) <br>
You may have to pip install dependencies such as uvicorn, fastapi etc. <br><br>

## Current weather
Request: POST localhost:8000/current <br><br>

Body: { <br>
    location: str <br>
} <br><br>

Response: https://openweathermap.org/current#example_JSON<br><br>

## Forecast
Request: POST localhost:8000/forecast<br><br>

Body: {<br>
    location: str<br>
    forecastType: str<br>
    variables: list[str]<br>
}<br><br>

Response: {<br>
        success: bool<br>
        temperature: list[float] (optional, only if requested)<br>
        humidity: list[float] (optional, only if requested)<br>
        precipitation: list[float] (optional, only if requested)<br>
}<br><br>

## Getting location, forecastType and variables
Request: GET localhost:8000/location<br>
Request: GET localhost:8000/forecastTypes<br>
Request: GET localhost:8000/variables<br>