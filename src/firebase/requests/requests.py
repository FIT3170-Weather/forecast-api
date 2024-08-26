import firebase_admin
from firebase_admin import firestore
from firebase_admin import credentials
from fastapi import APIRouter
from src.firebase.response_models.responses import *
from src.current.requests.requests import *
from fastapi import FastAPI, HTTPException, Depends, Header

# Initilizes Firebase Admin SDK
cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred)

# Initilizes Firestore
db = firestore.client()

# Sets FastAPI's router
router = APIRouter()

#TODO: Change default profile data (refer to firestore)
#      (Daryl) create API for location calling and alerts and email thingy
#      (Hani) edit API to accept a JSON containing a list of locations (str) 
#             change the "locations" db thingy
#             change update_alerts API to change the boolean in the database based on request


# Default profile data, edits can be done if wanted to
default_profile_data = {

    "locations": ["kuala-lumpur", "petaling-jaya", "subang-jaya"],

    "profile_data": {
        "alerts": False,
        "email": "",
        "home_location": "",
        "username": "",
    },
}


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
@router.get("/profiles")
async def getProfiles():
    try:
        res = []
        docs = db.collection("test_profiles").stream()
        for doc in docs:
            data_dict = doc.to_dict()
            locations_data = data_dict.get('locations', [])
            profile = {
                "uid": doc.id,
                "locations": locations_data,
                "profile_data": data_dict.get('profile_data', {})
            }
            res.append(profile)
        
        return {"status": "success", "data": res}
    except Exception as e:
        return {"status": "error", "error": e.message}



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
@router.post("/profiles/{uid}")
async def getProfile(uid: str):
    try:
        profile_ref = db.collection("profiles").document(uid)
        profile = profile_ref.get()
        res = {}
        
        if profile.exists:
            data_dict = profile.to_dict()
            res = {
                "uid": profile.id,
                "locations": data_dict.get('locations', []),
                "profile_data": data_dict.get('profile_data', {})
            }
            
            return {"status": "success", "data": res}
        else:
            return {"status": "error", "error":"Profile not found"}
    
    except Exception as e:
        return {"status": "error", "error": e.message}

    
"""
Returns a JSON of the preferences for the given UID

Takes:
    uid: str
    uid <- I7ze3UyWXqPB1S6HC0fGt6In7Nx1

Returns:
{
    "status":"success",
    "data":[
            "kuala-lumpur",
            "petaling-jaya",
            "subang-jaya"
    ]
    "error":null
}
"""    
@router.post("/profiles/{uid}/get_locations")
async def getPreferences(uid: str):
    try:
        profile_ref = db.collection("profiles").document(uid)
        profile = profile_ref.get()
        
        if profile.exists:
            data_dict = profile.to_dict()
            res = data_dict.get('locations')
            
            return {"status":"success", "data": res}
        else:
            return {"status": "error", "error": "Profile not found"}
    
    except Exception as e:
        return {"status": "error", "error": e.message}


@router.post("/profiles/{uid}/preferences/forecast")
async def getPreferencesForecast(uid: str):
    try:
        response = await getPreferences(uid)
        res = {}
        for loc in response.get('data'):
            
            res[loc] = await getCurrentWeather(currentBody(location=loc))
        return {"success": True, "data": res}

    except Exception as e:
        return {"success": False, "error": e.message}
    
"""
Returns a JSON of all subscribed emails

Return:
{
    "status":"success",
    "data":[
        [
            "email": email,
            [
                "kuala-lumpur",
                "petaling-jaya",
                "subang-jaya"
            ]
        ],
                [
            "email": second- email,
            [
                "kuala-lumpur",
            ]
        ]
    ]
    "error":null
}
"""    
@router.get("/profiles/subscriptions")
async def get_subscriptions():
    try:
        emails = []
        data = await getProfiles()
        profiles = data.get('data')

        for prof in profiles:
            profile = prof.get('profile_data')
            loc = prof.get('locations')
            print(prof)
            if profile.get('alerts'):
                emails.append([profile.get('email'), loc])

        return {"success": True, "data": emails}
        
    except Exception as e:
        return {"success": False, "error": str(e)}


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
        doc = profiles_ref.get()
        if not doc.exists:
            raise HTTPException(status_code=404, detail="Profile not found")

        # Retrieve the current profile_data
        current_data = doc.to_dict().get("profile_data", {})

        # Prepare the updated data, merging with the existing data
        update_data = {k: v for k, v in profile_data_update.dict().items() if v is not None}
        updated_profile_data = {**current_data, **update_data}

        # Update the profile_data field
        profiles_ref.update({"profile_data": updated_profile_data})

        return {"user_id": user_id, "message": "Profile data updated successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

#API to update locations
@router.put("/update_location/{user_id}")
async def update_location(user_id: str, locations_update: LocationsUpdate):
    try:
        profiles_ref = db.collection("profiles").document(user_id)

        # Check if the document exists
        if not profiles_ref.get().exists:
            raise HTTPException(status_code=404, detail="Profile not found")

        # Overwrite the locations array with the new one
        profiles_ref.update({"locations": locations_update.locations})

        return {"user_id": user_id, "message": "Locations updated successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
#API to update alerts
@router.put("/update_alert/{user_id}")
async def update_alert(user_id: str, alert_update: AlertUpdate):
    try:
        profiles_ref = db.collection("profiles").document(user_id)

        # Check if the document exists
        doc = profiles_ref.get()
        if not doc.exists:
            raise HTTPException(status_code=404, detail="Profile not found")

        # Update the alerts field in profile_data with the provided value
        profiles_ref.update({"profile_data.alerts": alert_update.alerts})

        return {
            "user_id": user_id,
            "message": f"Alert state updated to {alert_update.alerts}"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

