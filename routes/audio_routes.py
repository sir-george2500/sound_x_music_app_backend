from bson import ObjectId
from fastapi import APIRouter, HTTPException, UploadFile
from db_query.audio_query import (
    read_audio_metadata, save_song_data, save_song_metadata, add_song_id, 
    upload_audio_to_s3, check_in_db_song
)
from models.song import SongUploadForm, AddSongIdMetatdataId

audio_router = APIRouter()

@audio_router.post("/upload_song_data")
async def upload_song(data: SongUploadForm):
    if check_in_db_song('songs_information', title=data.title):
        raise HTTPException(status_code=400, detail="Song data already exists")

    try:
        saveSong = await save_song_data(data)
        return saveSong
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error uploading song: {str(e)}")

@audio_router.post("/upload_song")
async def read_file_route(file: UploadFile):
    try:
        content = await read_audio_metadata(file)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error reading song data: {str(e)}")

    if check_in_db_song('songs_metadata', file_name=content["file_name"]):
        raise HTTPException(status_code=400, detail="Song metadata already exists")

    file_size_mb = content["file_size"] / (1024 * 1024)
    if file_size_mb > 60.7:
        raise HTTPException(status_code=400, detail="Song metadata already exists")

    try:
        await save_song_metadata(content)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error saving song data: {str(e)}")

    try:
        result = await upload_audio_to_s3(file)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error uploading the song: {str(e)}")

@audio_router.post("/add_song_id")
async def add_song_id_endpoint(data: AddSongIdMetatdataId):
    try:
        songm_id_bson = ObjectId(data.songm_id)
        song_id = data.song_id
    except Exception as e:
        raise HTTPException(status_code=400, detail="Invalid songm_id format")

    song_in_db = check_in_db_song('songs_metadata', _id=song_id)

    if not song_in_db:
        raise HTTPException(status_code=400, detail="Invalid song ID")

    try:
        success = await add_song_id(songm_id_bson, song_id)
        return success
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error adding song ID: {str(e)}")
