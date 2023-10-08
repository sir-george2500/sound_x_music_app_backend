from pydantic import BaseModel, Field
from fastapi import UploadFile


class SongUploadForm(BaseModel):
    title: str = Field(..., description="Title of the song")
    artist: str = Field(..., description="Artist of the song")
    genre: str = Field(..., description="Genre of the song")
    song_price:str = Field(...,description="Price of the song")
    user_id:str

    class Config:
        json_schema_extra = {
            "examples": [
                {
                    "title": 'testsong',
                    "artist": 'codebeta2500@gmail.com',
                    "genre": 'rap-music',
                    "song_price": '200LRD',
                    "user_id":'650e6be8ed45ccde1f2eae68'

                },
            ]
        }

class AddSongIdMetatdataId(BaseModel):
      songm_id:str
      song_id:str
