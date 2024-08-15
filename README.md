# forecast-api

# Start up
Run "/main.py" (NOTE: NOT /src/main.py)
You may have to pip install dependencies such as uvicorn, fastapi etc.

## Current weather
Request: GET localhost:8000/current

Body: {
    location: str
}

Response: https://openweathermap.org/current#example_JSON

## Forecast
Request: GET localhost:8000/forecast

Body: {
    location: str
    forecastType: str
    variables: list[str]
}

Response: {
        success: bool
        temperature: list[float] (optional, only if requested)
        humidity: list[float] (optional, only if requested)
        precipitation: list[float] (optional, only if requested)
}

## Getting location, forecastType and variables
Request: GET localhost:8000/location
Request: GET localhost:8000/forecastTypes
Request: GET localhost:8000/variables