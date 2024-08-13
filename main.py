from fastapi import FastAPI, File, UploadFile
from pydantic import BaseModel
import locations.locations as loc

app = FastAPI()

@app.get("/locations")
async def hourly():
    return loc.Locations().getLocations()