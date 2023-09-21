from fastapi import APIRouter, Body, Request, Response, HTTPException, status
from config.db import client

router = APIRouter()

@router.get("/test_db_connection")
def test_db_connection():
    try:
        db = client["sound-x"]
        collection = db["users"]
        document = collection.find_one()
        return {"message": "Database connection successful!"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error connecting to database: {str(e)}")