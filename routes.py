from fastapi import APIRouter, HTTPException
from config.db import client
from models.user import RegisterUser
from db_query.query import testconnection, create_user

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
