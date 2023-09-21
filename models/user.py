from fastapi import FastAPI
from pydantic import BaseModel, Field

"""
Define all the Model relating to user 
"""

class RegisterUser(BaseModel):
    username: str = Field(..., description="Username of the user to register")
    email: str = Field(..., description="email of the user to register")
    password: str = Field(..., description="Password of the user to register")

    class Config:
        json_schema_extra = {
            "examples": [
                {
                    "username": "john_doe",
                    "email":"gsmulbah2500@gmail.com",
                    "password": "secret123"
                },
                {
                    "username": "alice_smith",
                    "password": "password456"
                }
            ]
        }


class LoginUser(BaseModel):
    username: str = Field(..., description="Username of the user to log in")
    password: str = Field(..., description="Password of the user to log in")

    class Config:
        json_schema_extra = {
            "examples": [
                {
                    "username": "john_doe",
                    "password": "secret123"
                },
                {
                    "username": "alice_smith",
                    "password": "password456"
                }
            ]
        }
