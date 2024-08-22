from typing import List, Union
from pydantic import BaseModel


class ProfileDataUpdate(BaseModel):
    email: str = None
    password: str = None
    username: str = None


class LocationsUpdate(BaseModel):
    locations: list[str]


class AlertUpdate(BaseModel):
    alerts: bool
