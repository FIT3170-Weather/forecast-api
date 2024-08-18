#BRO!! I have no idea where to do my fucking APIs so I'm doing it here,
# if I'm wrong(DEFINITELY) please guide me -- Hanideepu

from fastapi import FastAPI, HTTPException, Depends, Header
import firebase_admin._auth_utils
import firebase_admin.auth
from pydantic import BaseModel
from firebase_config import db
import firebase_admin
from firebase_admin import auth

app = FastAPI()

# Default profile data, edits can be done if wanted to
default_profile_data = {
    "alerts": {
        "rain": True,
        "wind": True,
        "thunderstorms": True,
        "temparature": True,
    },
    "preferences": {
        "locations": ["kuala-lumpur", "petaling-jaya", "subang-jaya"],
    },
    "profile_data": {
        "email": "",
        "password": "",
        "username": "",
    },
}

    
#API to create user
@app.post("/create_profile/{user_id}")
async def create_profile(user_id: str):
    try:
        # Yeah man this is how we get the collection "profiles"
        profiles_ref = db.collection("profiles")

        # Checking if document with user_id already exists, if so then outta here
        doc = profiles_ref.document(user_id).get()
        if doc.exists:
            raise HTTPException(status_code=400, detail="Profile already exists")

        # Yeah after that just add default data to that user under that document
        profiles_ref.document(user_id).set(default_profile_data)

        return {"user_id": user_id, "message": "Profile created successfully with default values"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
class ProfileDataUpdate(BaseModel):
    email: str = None
    password: str = None
    username: str = None

@app.put("/update_profile_data/{user_id}")
async def update_profile_data(user_id: str, profile_data_update: ProfileDataUpdate):
    try:
        profiles_ref = db.collection("profiles").document(user_id)

        # Check if the document exists
        if not profiles_ref.get().exists:
            raise HTTPException(status_code=404, detail="Profile not found")

        # Prepare the updated data
        update_data = {k: v for k, v in profile_data_update.dict().items() if v is not None}

        # Update the profile_data field
        profiles_ref.update({"profile_data": update_data})
        
        return {"user_id": user_id, "message": "Profile data updated successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

class LocationUpdate(BaseModel):
    location: str

@app.put("/add_location/{user_id}")
async def add_location(user_id: str, location_update: LocationUpdate):
    try:
        profiles_ref = db.collection("profiles").document(user_id)

        # Check if the document exists
        if not profiles_ref.get().exists:
            raise HTTPException(status_code=404, detail="Profile not found")

        # Add the new location to the locations list
        profiles_ref.update({
            "preferences.locations": firebase_admin.firestore.ArrayUnion([location_update.location])
        })

        return {"user_id": user_id, "message": "Location added successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    

class AlertUpdate(BaseModel):
    alert_type: str
    state: bool  # Allows specifying whether to set the alert to true or false

@app.put("/update_alert/{user_id}")
async def update_alert(user_id: str, alert_update: AlertUpdate):
    try:
        profiles_ref = db.collection("profiles").document(user_id)

        # Check if the document exists
        if not profiles_ref.get().exists:
            raise HTTPException(status_code=404, detail="Profile not found")

        # Retrieve the current alerts
        current_data = profiles_ref.get().to_dict()
        alerts = current_data.get("alerts", {})

        # Update the alert (whether it exists or is new)
        alerts[alert_update.alert_type] = alert_update.state

        # Apply the update to Firestore
        profiles_ref.update({"alerts": alerts})

        return {"user_id": user_id, "message": f"{alert_update.alert_type} alert set to {alert_update.state}"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))




if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
