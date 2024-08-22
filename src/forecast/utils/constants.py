# Description: Constants used in the forecast module

FORECAST_PREV_DAYS = 3 # Past 3 days for inference
FORECAST_CURRENT_DAYS = 1 # This means the current day also used in inference
DAYS_TO_FORECAST = 7
TIMEZONE = 'Asia/Singapore'
PREDICTED_ATTRIBUTES = ['temperature_2m', 'relative_humidity_2m', 'dew_point_2m', 'rain', 'pressure_msl', 'wind_speed_10m', 'wind_direction_10m']
