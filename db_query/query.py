from config.db import client
from passlib.hash import bcrypt 
from datetime import datetime, timedelta
from dotenv  import load_dotenv
import os
import jwt

# Load environment variables from .env
load_dotenv()

 


#gobal variable 
SECRET_KEY = os.getenv("Secret_Key")  
ALGORITHM = "HS256"

#test if the database is connected
def testconnection():
        db = client["sound-x"]
        collection = db["users"]
        document = collection.find_one()
        return {"message": "Database connection successful!"}

# Create the user
def create_user(user_data):
    db = client["sound-x"]
    users_collection = db["users"]

    # check if the user exists in the DB
    if users_collection.find_one({'$or': [{'email': user_data.username}, {'email': user_data.email}]}):
        return {"error": "Username or email already exists"}

    # Hash the password before storing it
    hashed_password = bcrypt.hash(user_data.password)
    user_data.password = hashed_password  

    # go ahead and create the user
    user_id = users_collection.insert_one(user_data.dict()).inserted_id
    return {"user_id": str(user_id)}





# ... (previous code remains the same) ...

def sign_user(user_data):
    db = client["sound-x"]
    users_collection = db["users"]

    # Find the user by username or email
    user = users_collection.find_one({'email': user_data.email})

    if user and bcrypt.verify(user_data.password, user['password']):
        # Generate a JWT token
        payload = {
            'user_id': str(user['_id']),
            'exp': datetime.utcnow() + timedelta(hours=1) 
        }

        jwt_token = jwt.encode(payload,SECRET_KEY, algorithm=ALGORITHM)  

        return {'jwt_token': jwt_token}
    else:
        return {"error": "Invalid username/email or password"}

# sign in google user by generating jwt token for them     
def sign_user_with_google(user_data):
    db = client["sound-x"]
    users_collection = db["third_party_users"]

    # Check if the user exists in the DB
    existing_user = users_collection.find_one({'$or': [{'email': user_data.email}, {'sub': user_data.sub}]})

    if existing_user:
        # Generate a JWT token
        payload = {
            'user_id': str(existing_user['_id']),
            'exp': datetime.utcnow() + timedelta(hours=1) 
        }  
        jwt_token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)  

        return {'jwt_token': jwt_token}
    else:
        # User not found, store their credentials and generate a JWT token
        user_doc = {
            'username': user_data.username,
            'email': user_data.email,
            'profile_image': user_data.profile_image,
            'sub': user_data.sub
        }
        result = users_collection.insert_one(user_doc)
        user_id = str(result.inserted_id)

        payload = {
            'user_id': user_id,
            'exp': datetime.utcnow() + timedelta(hours=1) 
        }  
        jwt_token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)  

        return {'jwt_token': jwt_token}
    

