from typing import List, Union, Optional
from pydantic import BaseModel, Field


class ProfileDataUpdate(BaseModel):
    email: Optional[str] = None
    home_location: Optional[str] = Field(None, alias="home-location")
    username: Optional[str] = None


class LocationsUpdate(BaseModel):
    locations: list[str]


class AlertUpdate(BaseModel):
    alerts: bool
