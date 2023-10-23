# Import necessary modules and libraries
from config.db import client
from datetime import datetime, timedelta
from config.db import client
from passlib.hash import bcrypt 
from fastapi import APIRouter, HTTPException
from .authenticate_users import (check_in_db, create_user )
#db client
db = client["sound-x"]



def verify_token(email, token):
    user_in_db = check_in_db('users', delimiter=1, email=email, reset_token=token)
    if not user_in_db:
        raise HTTPException(status_code=404, detail="Token not found")
    current_time = datetime.utcnow()
    token_expiry = user_in_db.get('token_expiry')
    if token_expiry and token_expiry > current_time:
        return True
    else:
        raise HTTPException(status_code=401, detail="Invalid Token")

def register_new_user(user_data):
    username = user_data.username
    email = user_data.email

    user_in_db = check_in_db('users', username=username, email=email)
    if user_in_db:
        raise HTTPException(status_code=400, detail="Username or email already exists")

    try:
        user_id = create_user(user_data)
        return {"user_id": user_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error registering user: {str(e)}")




