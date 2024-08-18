import firebase_admin
from firebase_admin import firestore
from firebase_admin import credentials
from fastapi import APIRouter
from src.firebase.response_models.responses import *
from fastapi import FastAPI, HTTPException, Depends, Header

# Initilizes Firebase Admin SDK
cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred)

# Initilizes Firestore
db = firestore.client()

# Sets FastAPI's router
router = APIRouter()


"""
Returns a JSON of every profile there is in the database

Returns:
{
    "status":"success",
    "data":[{
        "uid":"I7ze3UyWXqPB1S6HC0fGt6In7Nx1",
        "alerts":{
            "thunder":true,
            "rain":true
        },
        "preferences":{
            "locations":[
                "kuala-lumpur",
                "petaling-jaya",
                "subang-jaya"
            ]
        },
        "profile_data":{
            "email":"",
            "password":"",
            "username":""
        }
    }],
    "error":null
}
"""
@router.get("/profiles", response_model=Response)
async def getProfiles():
    try:
        res = []
        docs = db.collection("profiles").stream()
        for doc in docs:
            data_dict = doc.to_dict()
            profile = ProfileDocument(
                uid = doc.id,
                alerts=Alerts(**data_dict.get('alerts', {})),
                preferences=Preferences(**data_dict.get('preferences', {})),
                profile_data=ProfileData(**data_dict.get('profile_data', {}))
            )
            res.append(profile.model_dump())
        
        return Response(status="success", data=res)
    except Exception as e:
        return Response(status="error", error=f"An error occurred: {str(e)}")



"""
Returns a JSON of the profile specified by the UID

Takes:
    uid: str
    uid <- I7ze3UyWXqPB1S6HC0fGt6In7Nx1

Returns:
{
    "status":"success",
    "data":[{
        "uid":"I7ze3UyWXqPB1S6HC0fGt6In7Nx1",
        "alerts":{
            "thunder":true,
            "rain":true
        },
        "preferences":{
            "locations":[
                "kuala-lumpur",
                "petaling-jaya",
                "subang-jaya"
            ]
        },
        "profile_data":{
            "email":"",
            "password":"",
            "username":""
        }
    }],
    "error":null
}
"""
@router.get("/profiles/{uid}", response_model=Response)
async def getProfiles(uid: str):
    try:
        profile_ref = db.collection("profiles").document(uid)
        profile = profile_ref.get()
        
        if profile.exists:
            data_dict = profile.to_dict()
            res = [ProfileDocument(
                uid=profile.id,
                alerts=Alerts(**data_dict.get('alerts', {})),
                preferences=Preferences(**data_dict.get('preferences', {})),
                profile_data=ProfileData(**data_dict.get('profile_data', {}))
            )]
            
            return Response(status="success", data=res)
        else:
            return Response(status="error", error="Profile not found")
    
    except Exception as e:
        return Response(status="error", error=f"An error occurred: {str(e)}")
    
    
"""
Returns a JSON of the alerts for the given UID

Takes:
    uid: str
    uid <- I7ze3UyWXqPB1S6HC0fGt6In7Nx1

Returns:
{
    "status":"success",
    "data":{
        "thunder":true,
        "rain":true
    },
    "error":null
}
"""    
@router.get("/profiles/{uid}/alerts", response_model=AlertsResponse)
async def getAlerts(uid: str):
    try:
        profile_ref = db.collection("profiles").document(uid)
        profile = profile_ref.get()
        
        
        if profile.exists:
            data_dict = profile.to_dict()
            res = Alerts(**data_dict.get('alerts', {}))
            
            return AlertsResponse(status="success", data=res)
        else:
            return AlertsResponse(status="error", error="Profile not found")
    
    except Exception as e:
        return AlertsResponse(status="error", error=f"An error occurred: {str(e)}")
    
    
"""
Returns a JSON of the preferences for the given UID

Takes:
    uid: str
    uid <- I7ze3UyWXqPB1S6HC0fGt6In7Nx1

Returns:
{
    "status":"success",
    "data":{
        "locations":[
            "kuala-lumpur",
            "petaling-jaya",
            "subang-jaya"
        ]
    },
    "error":null
}
"""    
@router.get("/profiles/{uid}/preferences", response_model=PreferencesResponse)
async def getPreferences(uid: str):
    try:
        profile_ref = db.collection("profiles").document(uid)
        profile = profile_ref.get()
        
        if profile.exists:
            data_dict = profile.to_dict()
            res = Preferences(**data_dict.get('preferences', {}))
            
            return PreferencesResponse(status="success", data=res)
        else:
            return PreferencesResponse(status="error", error="Profile not found")
    
    except Exception as e:
        return PreferencesResponse(status="error", error=f"An error occurred: {str(e)}")

#TODO: Create a template for the default profile creation
#TODO: Implement the google sign in method
#TODO: Implement the POST method to write data into the DATABASE
#TODO: Implement the PUT method to update the data in the DATABASE
#TODO: Upon login/account creation, check if the profile exists in the database, if not, create a new profile using the template and assign default values.



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
@router.post("/create_profile/{user_id}")
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
    
#API to update user details
@router.put("/update_profile_data/{user_id}")
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

#API to add preferrence location
@router.put("/add_location/{user_id}")
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
    
#API to update or create alerts
@router.put("/update_alert/{user_id}")
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