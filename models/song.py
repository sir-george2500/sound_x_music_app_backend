from pydantic import BaseModel, Field
from fastapi import UploadFile


class SongUpload(BaseModel):
    title: str = Field(..., description="Title of the song")
    artist: str = Field(..., description="Artist of the song")
    genre: str = Field(..., description="Genre of the song")
    song_file: UploadFile = Field(..., description="The song file")
    cover_image: UploadFile = Field(..., description="Cover image for the song")

