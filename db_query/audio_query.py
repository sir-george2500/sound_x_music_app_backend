import io
import librosa
from config.db import client

from fastapi import UploadFile

async def read_audio_metadata(file: UploadFile):
    """Read metadata of an audio file uploaded by the client."""

    # Read the contents of the uploaded file.
    audio_content = await file.read()

    # Extract file name and type from the UploadFile object.
    file_name = file.filename
    file_type = file.content_type
    file_size = file.size

    # Create a BytesIO object to hold the audio data.
    audio_io = io.BytesIO(audio_content)

    # Read the audio file using Librosa to get metadata.
    audio_data, sample_rate = librosa.load(audio_io, sr=None)

    # Get the duration of the audio file.
    duration = librosa.get_duration(y=audio_data, sr=sample_rate)

    # Return the metadata including file name and type.
    return {
        "file_name": file_name,
        "file_type": file_type,
        "file_size": file_size,
        "sample_rate": sample_rate,
        "duration": duration

    }


#save song data 
async def save_song_data(data):
    db = client["sound-x"]
    song_collection = db["songs_information"]

    # Check if a song with the same title already exists
    if song_collection.find_one({'title': data.title}):
        return {"Error":"Song with the same title already exists"}

    # If not, insert the new song data
    song_id = song_collection.insert_one(data.dict()).inserted_id
    return {"song_id": str(song_id)}

#save song metadata 
async def save_song_metadata(data):
    db = client["sound-x"]
    song_collection = db["songs_metadata"]

    # Check if a song with the same file name in it metadata already exists
    if song_collection.find_one({'file_name': data["file_name"]}):
        return {"Error":"Song with the same title already exists"}

    # If not, insert the new song metadata
    songmd_id = song_collection.insert_one(data).inserted_id
    return {"song_metadata_id": str(songmd_id)}

    



  



