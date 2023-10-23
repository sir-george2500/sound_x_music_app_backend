from fastapi import APIRouter, HTTPException
from datetime import datetime

from db_query.auth.authenticate_users import (
    create_user, sign_user, sign_user_with_google, get_user_data, 
    check_in_db, is_valid_user, update_request_token, send_reset_password_email
)
from db_query.auth.auth_users_route_logic import (
  verify_token, register_new_user, authenticate_user
)

from models.user import (
    RegisterUser, LoginUser, LoginGoogleUser, 
    ResetTokenRequest, VerifyToken)

auth_router = APIRouter()

@auth_router.post("/register_user")
def register_user(user: RegisterUser):
    return register_new_user(user)


@auth_router.post("/login_user")
def login_user(user: LoginUser):
    return authenticate_user(user)


@auth_router.post("/login_with_google")
def login_with_google(user: LoginGoogleUser):
    try:
        jwt = sign_user_with_google(user)
        return {"jwt": jwt}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error login user: {str(e)}")

@auth_router.get("/get_user_data/{email}")
async def get_user(email: str):
    user_data = await get_user_data(email)
    if user_data is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user_data

@auth_router.post("/request_reset_token")
async def request_reset_token(user: ResetTokenRequest):
    email = user.email
    
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




@auth_router.post("/verify_token")
async def verify_reset_token(data: VerifyToken):
    email = data.email
    token = data.token
    return verify_token(email, token)


# @auth_router.post("/change_password")
# async def change_password(data:):
#  token = data.token

#  if not  validate_token(token):
#          raise HTTPException(status_code=401, detail=f"Invalid Token")

#  return True






    

 

 




