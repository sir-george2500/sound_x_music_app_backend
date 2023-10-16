# Imports should be organized in separate lines and grouped by their origin (standard library, third-party, local).
from bson import ObjectId
from config.db import client
from fastapi import APIRouter, HTTPException, UploadFile
from db_query.authenticate_user_query import (
    test_connection, create_user, sign_user, sign_user_with_google, get_user_data, check_in_db, is_valid_user
)
from db_query.audio_query import (
    read_audio_metadata, save_song_data, save_song_metadata, add_song_id, upload_audio_to_s3
)
from models.user import RegisterUser, LoginUser, LoginGoogleUser, ResetTokenRequest
from models.song import SongUploadForm, AddSongIdMetatdataId


# Create an instance of APIRouter
router = APIRouter()

db = client["sound-x"]

# Endpoint to test the database connection
@router.get("/test_db_connection")
def test_db_connection():
    try:
        return test_connection()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error connecting to database: {str(e)}")


# Endpoint to register a new user
@router.post("/register_user")
def register_user(user: RegisterUser):
    # Check if the user already exists in the DB
    user_in_db = check_in_db('users', username=user.username, email=user.email)
    if user_in_db:
        raise HTTPException(status_code=400, detail="Username or email already exists")

    try:
        # Create the user in the database
        user_id = create_user(user)
        return {"user_id": user_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error registering user: {str(e)}")


# Endpoint to log in a user
@router.post("/login_user")
def login_user(user: LoginUser):

    if not is_valid_user(user):
        raise HTTPException(status_code= 401, detail="Invalid password or Username")
    try:
        # Create the user in the database
        jwt = sign_user(user)
        return {"jwt": jwt}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error login user: {str(e)}")


# Endpoint to log in a user with Google
@router.post("/login_with_google")
def login_with_google(user: LoginGoogleUser):
    try:
        # Create the user in the database
        jwt = sign_user_with_google(user)
        return {"jwt": jwt}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error login user: {str(e)}")


# Endpoint to get user data by email
@router.get("/get_user_data/{email}")
async def get_user(email: str):
    user_data = await get_user_data(email)
    if user_data is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user_data


# Endpoint to upload song data
@router.post("/upload_song_data")
async def upload_song(data: SongUploadForm):
    try:
        saveSong = await save_song_data(data)
        return saveSong
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error uploading song: {str(e)}")


# Endpoint to read and process an uploaded audio file
@router.post("/upload_song")
async def read_file_route(file: UploadFile):
    """Read an audio file from the client's computer."""
    try:
        content = await read_audio_metadata(file)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error reading song data: {str(e)}")

    try:
        await save_song_metadata(content)
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error saving song data: {str(e)}")
    
    try:
        result=await upload_audio_to_s3(file)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error uploading the song: {str(e)}")
    
  
    

# Endpoint to add a song ID to song metadata record
@router.post("/add_song_id")
async def add_song_id_endpoint(data:AddSongIdMetatdataId):   
    try:
        songm_id_bson = ObjectId(data.songm_id)
        song_id = data.song_id
    except Exception as e:
        raise HTTPException(status_code=400, detail="Invalid songm_id format")

    try:
        success = await add_song_id(songm_id_bson,song_id)
        return success
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error adding song ID: {str(e)}")




@router.post("/request_reset_token")
async def request_reset_token(user: ResetTokenRequest):
    email = user.email
    
    #check if the user is in the database
    user_in_db = check_in_db('users', email=email)

    if not user_in_db:
        raise HTTPException(status_code=404, detail=f"User not found")
    return {"message": f"Successfully added the field to the db"}

