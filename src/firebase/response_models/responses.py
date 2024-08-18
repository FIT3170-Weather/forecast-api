from typing import List, Union
from pydantic import BaseModel


class Alerts(BaseModel):
    thunder: bool
    rain: bool

class Preferences(BaseModel):
    locations: List[str]

class ProfileData(BaseModel):
    email: str
    password: str
    username: str

class ProfileDocument(BaseModel):
    uid: str
    alerts: Alerts
    preferences: Preferences
    profile_data: ProfileData

class Response(BaseModel):
    status: str
    data: Union[List[ProfileDocument], None] = None
    error: Union[str, None] = None

class AlertsResponse(BaseModel):
    status: str
    data: Alerts
    error: Union[str, None] = None
    
class PreferencesResponse(BaseModel):
    status: str
    data: Preferences
    error: Union[str, None] = None


