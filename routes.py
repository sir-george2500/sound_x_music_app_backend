from fastapi import APIRouter, HTTPException
from config.db import client
from models.user import RegisterUser ,LoginUser,LoginGoogleUser
from db_query.query import testconnection, create_user , sign_user, sign_user_with_google

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
    
