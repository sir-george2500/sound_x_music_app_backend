# Import necessary modules and libraries
from config.db import client
from datetime import datetime, timedelta
from config.db import client
from passlib.hash import bcrypt 
from fastapi import APIRouter, HTTPException
from .authenticate_users import (
    check_in_db, create_user, is_valid_user,
    sign_user, sign_user_with_google, get_user_data,
    update_request_token, send_reset_password_email )

#db client
db = client["sound-x"]


def register_new_user(user_data):
    """
    Register a new user.

    Args:
        user_data (UserData): User data containing username, email, and password.

    Returns:
        dict: User ID.

    Raises:
        HTTPException: If the username or email already exists 
        or 
        if there's an error registering the user.
    """
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


def authenticate_user(user):
    """
    Authenticate a user.

    Args:
        user (UserCredentials): User credentials containing username and password.

    Returns:
        dict: JWT token.

    Raises:
        HTTPException: If the user credentials are invalid 
        or 
        if there's an error during authentication.
    """
    if not is_valid_user(user):
        raise HTTPException(status_code=401, detail="Invalid password or Username")
    try:
        jwt = sign_user(user)
        return {"jwt": jwt}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error login user: {str(e)}")

def authenticate_user_with_google(user):
    """
    Authenticate a user using Google.

    Args:
        user (GoogleUserCredentials): User credentials from Google.

    Returns:
        dict: JWT token.

    Raises:
        HTTPException: If there's an error during authentication.
    """
    try:
        jwt = sign_user_with_google(user)
        return {"jwt": jwt}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error login user: {str(e)}")

async def fetch_user_data(email):
    """
    Fetch user data by email.

    Args:
        email (str): User's email.

    Returns:
        dict: User data.

    Raises:
        HTTPException: If the user is not found.
    """
    user_data = await get_user_data(email)
    if user_data is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user_data


async def process_reset_token_request(email):
    """
    Process request for resetting the token.

    Args:
        email (str): User's email.

    Returns:
        str: Result of the reset process.

    Raises:
        HTTPException: If there's an error generating the token 
        or 
        sending the mail.
    """
    user_in_db = check_in_db('users', email=email)

    if not user_in_db:
        raise HTTPException(status_code=404, detail="User not found")

    try:
        result = await update_request_token(email)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating the token: {e}")
   
    try:
        sent = await send_reset_password_email(email, result)
        return sent
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"error sending the mail {e}")


def verify_token(email, token):
    """
    Verify token validity.

    Args:
        email (str): User's email.
        token (str): Reset token.

    Returns:
        bool: True if token is valid, else raises HTTPException.

    Raises:
        HTTPException: If the token is not found or invalid.
    """
    user_in_db = check_in_db('users', delimiter=1, email=email, reset_token=token)
    if not user_in_db:
        raise HTTPException(status_code=404, detail="Token not found")
    current_time = datetime.utcnow()
    token_expiry = user_in_db.get('token_expiry')
    if token_expiry and token_expiry > current_time:
        return True
    else:
        raise HTTPException(status_code=401, detail="Invalid Token")

