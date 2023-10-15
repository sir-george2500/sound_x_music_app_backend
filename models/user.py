from pydantic import BaseModel, Field

"""
Define all the Model relating to user 
"""

class RegisterUser(BaseModel):
    username: str = Field(..., description="Username of the user to register")
    email: str = Field(..., description="email of the user to register")
    password: str = Field(..., description="Password of the user to register")
    profile_image: str = Field(..., description="Password of the user to register")
    reset_token: str = Field(..., description="Reset Token")
    token_expiry: str = Field(..., description="Token expiry")



    class Config:
        json_schema_extra = {
            "examples": [
                {
                    "username": "john_doe",
                    "email":"gsmulbah2500@gmail.com",
                    "password": "secret123",
                    "profile_image":"None",
                    "reset_token" : "None",
                    "token_expiry":"None"
                },
            ]
        }


class LoginUser(BaseModel):
    email: str = Field(..., description="email of the user to log in")
    password: str = Field(..., description="Password of the user to log in")

    class Config:
        json_schema_extra = {
            "examples": [
                {
                    "email": "gsmulbah2500@gmail.com",
                    "password": "secret123"
                },
                {
                    "email": "game2500@gmail.com",
                    "password": "password456"
                }
            ]
        }

class LoginGoogleUser(BaseModel):
    username:str = Field(..., description="username  of the google user to log in")
    email: str = Field(..., description="email of the google user to  log in")
    profile_image: str = Field(..., description="profile image of that google user")
    sub: str = Field(...,description="sub for google user")

    class Config:
        json_schema_extra = {
            "examples": [
                {
                    "username": 'coder-x',
                    "email": 'codebeta2500@gmail.com',
                    "profile_image": 'https://lh3.googleusercontent.com/a/ACg8ocJYUbgeMobRRlOwkw7rOCiFwUVNS4OcPz__TzjakLoD=s96-c',
                    "sub": '113442546591326061804',

                },
            ]
        }

class ResetTokenRequest(BaseModel):
    email: str

    class Config:
        json_schema_extra = {
            "examples": [
                {                
                    "email": 'codebeta2500@gmail.com',
                },
            ]
        }