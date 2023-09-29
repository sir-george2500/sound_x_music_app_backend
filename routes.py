import librosa
from fastapi import APIRouter, HTTPException,UploadFile
from config.db import client
from models.user import RegisterUser ,LoginUser,LoginGoogleUser
from models.song import SongUploadForm
from db_query.authenticate_user_query import testconnection, create_user , sign_user, sign_user_with_google ,get_user_data
from db_query.audio_query import read_audio_metadata,save_song_data,save_song_metadata
import json

router = APIRouter()

@router.get("/test_db_connection")
def test_db_connection():
    try:
        return testconnection() 
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error connecting to database: {str(e)}")

@router.post("/register_user")
def register_user(user: RegisterUser):
    try:
        # Create the user in the database
        user_id = create_user(user)
        return {"user_id": user_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error registering user: {str(e)}")
    
@router.post("/login_user")
def login_user(user:LoginUser):
    try:
        # Create the user in the database
        jwt = sign_user(user)
        return {"jwt": jwt}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error login user: {str(e)}")
    
@router.post("/login_with_google")
def login_with_google(user:LoginGoogleUser):
    try:
        # Create the user in the database
        jwt= sign_user_with_google(user)
        return {"jwt": jwt}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error login user: {str(e)}")

@router.get("/get_user_data/{email}")
async def get_user(email: str):
    user_data = await get_user_data(email)
    if user_data is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user_data


@router.post("/upload_song_data")
async def upload_song(data:SongUploadForm):
    try:
       saveSong= await save_song_data(data)
       return saveSong
    except Exception as e:
         raise HTTPException(status_code=500, detail=f"Error uploading song:{str(e)}")

@router.post("/upload_song")
async def read_file_route(file: UploadFile):
    """Read an audio file from the client's computer."""
    try:
        content = await read_audio_metadata(file)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error reading song data: {str(e)}")

    try:
        result = await save_song_metadata(content)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error saving song data: {str(e)}")
   


