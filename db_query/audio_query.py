# import necessary modules and libraries
import io
import librosa
from config.db import client
import boto3
from dotenv import load_dotenv
import os

from fastapi import UploadFile


# Load environment variables
load_dotenv()



# Access environment variables
AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
S3_BUCKET_NAME = os.getenv("S3_BUCKET_NAME")

# using these credential
s3 = boto3.client(
    's3',
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY
)

# Global Variable 
db = client["sound-x"]


# variadic  function for checking in the Database for song info
def check_in_db_song(collection, delimiter=0, **kwargs):
    """
    Check if a user exists in the database.

    Args:
        collection (str): Name of the collection to search in.
        delimiter (int): A value to determine the search type.
        **kwargs: Keyword arguments representing field names and their corresponding values for the search.

    Returns:
        The user document if found, otherwise None.
    """
    song_collection = db[collection]
  
    if delimiter > 0:
        query = {'title': kwargs.get('title')}
    else:
        or_conditions = [{field: value} for field, value in kwargs.items()]
        query = {'$or': or_conditions}

    song_in_db = song_collection.find_one(query)
    return song_in_db


# Function to read metadata of an uploaded audio file
async def read_audio_metadata(file: UploadFile):
    """
    Read metadata of an audio file uploaded by the client.

    Args:
        file: The uploaded audio file.

    Returns:
        Metadata of the audio file.
    """

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


# Function to save song data in the database
async def save_song_data(data):
    """
    Save song data to the database.

    Args:
        data: Song data to be saved.

    Returns:
        Song ID if saved successfully, else an error message.
    """

    song_collection = db["songs_information"]
    # If not, insert the new song data
    song_id = song_collection.insert_one(data.dict()).inserted_id
    return {"song_id": str(song_id)}


# Function to save song metadata in the database
async def save_song_metadata(data):
    """
    Save song metadata to the database.

    Args:
        data: Song metadata to be saved.

    Returns:
        Song metadata ID if saved successfully, else an error message.
    """

    song_collection = db["songs_metadata"]

    data["song_id"] = "None"

    # Check if a song with the same file name in its metadata already exists
    if song_collection.find_one({'file_name': data["file_name"]}):
        return {"Error": "Song with the same title already exists"}

    # If not, insert the new song metadata
    song_collection.insert_one(data).inserted_id

async def upload_audio_to_s3(file: UploadFile):

    """
    Adds the song file to amazon s3 bucket.

    Args:
        file: the file to be uploaded.

    Returns:
        File uploaded successfully
    """
    # Read the contents of the uploaded file.
    audio_content = await file.read()

    # Extract file name from the UploadFile object.
    file_name = file.filename

    # Upload the file to S3
    s3.upload_fileobj(io.BytesIO(audio_content), S3_BUCKET_NAME, file_name)

    # Generate a pre-signed URL for the uploaded file
    url = s3.generate_presigned_url('get_object', Params={'Bucket': S3_BUCKET_NAME, 'Key': file_name})
    return {"message": "File uploaded successfully", "url": url}
    


# Function to add a song ID to song metadata record
async def add_song_id(songm_id,song_id):
    """
    Adds the song ID to the song metadata record.

    Args:
        songm_id: The ID of the song metadata record.

    Returns:
        0 if the song ID was added successfully, 1 otherwise.
    """

    db = client["sound-x"]
    songm_collection = db["songs_metadata"]

    if songm_collection.find_one({"_id": songm_id}):
        songm_collection.update_one({"_id": songm_id}, {"$set": {"song_id": song_id}})
        return {"success": 0}
    else:
        return {"success": 1, "error": "Song metadata record does not exist."}


