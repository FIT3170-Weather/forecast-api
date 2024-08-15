from fastapi import FastAPI
from pydantic import BaseModel
import src.forecast.bodyParameters.locations as loc
from .current.requests import requests as current
from .forecast.requests import requests as forecast
from .firebase.requests import requests as firebase

app = FastAPI() # DO NOT RUN FROM HERE; run /main.py instead

app.include_router(current.router)
app.include_router(forecast.router)
app.include_router(firebase.router)