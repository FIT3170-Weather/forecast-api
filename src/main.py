from fastapi import FastAPI
from pydantic import BaseModel
import src.forecast.bodyParameters.locations as loc
from .historical.requests import requests as historical
from .current.requests import requests as current
from .forecast.requests import requests as forecast
from fastapi.middleware.cors import CORSMiddleware
from .firebase.requests import requests as firebase

app = FastAPI() # DO NOT RUN FROM HERE; run /main.py instead

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

app.include_router(historical.router)
app.include_router(current.router)
app.include_router(forecast.router)
app.include_router(firebase.router)