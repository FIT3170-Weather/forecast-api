from typing import List, Union
from pydantic import BaseModel


class Alerts(BaseModel):
    rain: bool
    heatwave: bool
    blizzard: bool
    thunderstorms: bool
    wind: bool

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

class ProfileDataUpdate(BaseModel):
    email: str = None
    password: str = None
    username: str = None

class LocationUpdate(BaseModel):
    location: str

class AlertUpdate(BaseModel):
    alert_type: str
    state: bool