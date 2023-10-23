from fastapi import APIRouter, HTTPException
from datetime import datetime

from db_query.auth.auth_users_route_logic import (
  validate_reset_token, register_new_user, authenticate_user,
  authenticate_user_with_google, fetch_user_data, process_reset_token_request,
  reset_password
)

from models.user import (
    RegisterUser, LoginUser, LoginGoogleUser, 
    ResetTokenRequest, VerifyToken, ResetPassword
    )

auth_router = APIRouter()


@auth_router.post("/register_user")
def register_user(user: RegisterUser):
    return register_new_user(user)


@auth_router.post("/login_user")
def login_user(user: LoginUser):
    return authenticate_user(user)


@auth_router.post("/login_with_google")
def login_with_google(user: LoginGoogleUser):
    return authenticate_user_with_google(user)


@auth_router.get("/get_user_data/{email}")
async def get_user_data_route(email: str):
    return await fetch_user_data(email)


@auth_router.post("/request_reset_token")
async def request_reset_token(user: ResetTokenRequest):
    return await process_reset_token_request(user)


@auth_router.post("/verify_token")
async def verify_reset_token(data: VerifyToken):
    return validate_reset_token(data)


@auth_router.post("/change_password")
async def change_password(data:ResetPassword):
    return reset_password(data)


   






    

 

 




