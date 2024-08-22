from typing import List, Union
from pydantic import BaseModel


class ProfileDataUpdate(BaseModel):
    email: str = None
    password: str = None
    username: str = None

class LocationUpdate(BaseModel):
    location: str

class AlertUpdate(BaseModel):
    alert_type: str
    state: bool