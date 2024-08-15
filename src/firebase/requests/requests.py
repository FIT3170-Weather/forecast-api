import firebase_admin
from firebase_admin import firestore
from firebase_admin import credentials
from fastapi import APIRouter
from src.firebase.response_models.responses import *


cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred)

db = firestore.client()
router = APIRouter()

@router.get("/profiles", response_model=Response)
async def getProfiles():
    try:
        res = []
        docs = db.collection("profiles").stream()
        for doc in docs:
            data_dict = doc.to_dict()
            # Print the data to debug

            # Validate and convert the data to Pydantic model
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



@router.get("/profiles/{uid}", response_model=Response)
async def getProfiles(uid: str):
    try:
        # Reference to the "profiles" collection
        profile_ref = db.collection("profiles").document(uid)
        
        # Get the document snapshot
        profile = profile_ref.get()
        
        # Check if the document exists
        if profile.exists:
            data_dict = profile.to_dict()
            res = [ProfileDocument(
                uid=profile.id,  # Correct field name for document ID
                alerts=Alerts(**data_dict.get('alerts', {})),
                preferences=Preferences(**data_dict.get('preferences', {})),
                profile_data=ProfileData(**data_dict.get('profile_data', {}))
            )]
            
            return Response(status="success", data=res)
        else:
            return Response(status="error", error="Profile not found")
    
    except Exception as e:
        return Response(status="error", error=f"An error occurred: {str(e)}")
    
@router.get("/profiles/{uid}/alerts", response_model=AlertsResponse)
async def getAlerts(uid: str):
    try:
        # Reference to the "profiles" collection
        profile_ref = db.collection("profiles").document(uid)
        
        # Get the document snapshot
        profile = profile_ref.get()
        
        
        # Check if the document exists
        if profile.exists:
            # Reference to the "alerts" subcollection
            data_dict = profile.to_dict()
            res = Alerts(**data_dict.get('alerts', {}))
            
            return AlertsResponse(status="success", data=res)
        else:
            return AlertsResponse(status="error", error="Profile not found")
    
    except Exception as e:
        return AlertsResponse(status="error", error=f"An error occurred: {str(e)}")
    
@router.get("/profiles/{uid}/preferences", response_model=PreferencesResponse)
async def getPreferences(uid: str):
    try:
        # Reference to the "profiles" collection
        profile_ref = db.collection("profiles").document(uid)
        
        # Get the document snapshot
        profile = profile_ref.get()
        
        
        # Check if the document exists
        if profile.exists:
            # Reference to the "alerts" subcollection
            data_dict = profile.to_dict()
            res = Preferences(**data_dict.get('preferences', {}))
            
            return PreferencesResponse(status="success", data=res)
        else:
            return PreferencesResponse(status="error", error="Profile not found")
    
    except Exception as e:
        return PreferencesResponse(status="error", error=f"An error occurred: {str(e)}")
    