import firebase_admin
from firebase_admin import firestore
from firebase_admin import credentials
from fastapi import APIRouter
from src.firebase.response_models.responses import *

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