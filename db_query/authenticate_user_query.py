# Import necessary modules and libraries
from config.db import client
from passlib.hash import bcrypt 
from datetime import datetime, timedelta
from dotenv  import load_dotenv
import os
import jwt
from datetime import datetime, timedelta
import uuid


# Load environment variables from .env
load_dotenv()

# Global variables for secret key and algorithm
SECRET_KEY = os.getenv("Secret_Key")  
ALGORITHM = "HS256"

#db client
db = client["sound-x"]

# variadic  function for checking in the Database for user
def check_in_db(collection, delimiter=0, **kwargs):
    """
    Check if a user exists in the database.

    Args:
        collection (str): Name of the collection to search in.
        delimiter (int): A value to determine the search type.
        **kwargs: Keyword arguments representing field names and their corresponding values for the search.

    Returns:
        The user document if found, otherwise None.
    """
    users_collection = db[collection]

    if delimiter > 0:
        query = {'email': kwargs.get('email')}
    else:
        or_conditions = [{field: value} for field, value in kwargs.items()]
        query = {'$or': or_conditions}

    user_in_db = users_collection.find_one(query)
    return user_in_db



# Test if the database is connected
def test_connection():
    """
    Test if the database connection is successful.

    Returns:
        A message indicating successful database connection.
    """
    collection = db["users"]
    document = collection.find_one()
    return {"message": "Database connection successful!"}

# Create a new user
def create_user(user_data):
    """
    Create a new user in the database.

    Args:
        user_data: User data including username, email, and password.

    Returns:
        A dictionary containing either the user_id or an error message.
    """
    users_collection = db["users"]

    hashed_password = bcrypt.hash(user_data.password)
    user_data.password = hashed_password  

    user_id = users_collection.insert_one(user_data.dict()).inserted_id
    return {"user_id": str(user_id)}

# Sign in a user
def sign_user(user_data):
    """
    Sign in a user and generate a JWT token.

    Args:
        user_data: User data including email and password.

    Returns:
        A dictionary containing a JWT token or an error message.
    """
    users_collection = db["users"]

    user = users_collection.find_one({'email': user_data.email})

    payload = {
        'user_id': str(user['_id']),
        'exp': datetime.utcnow() + timedelta(hours=1) 
    }

    jwt_token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)  

    return {'jwt_token': jwt_token}

def is_valid_user(user_data):
    """
    Check if a user is valid based on provided user data.

    Args:
        user_data (dict): Dictionary containing user data including email and password.

    Returns:
        bool: True if the user is valid, False otherwise.
    """
    users_collection = db["users"]

    # Find the user by email
    user = users_collection.find_one({'email': user_data.email})

    # Check if user exists and password is valid
    if user and bcrypt.verify(user_data.password, user['password']):
        return True

    return False


# Sign in a user with Google credentials and generate a JWT token
def sign_user_with_google(user_data):
    """
    Sign in a user with Google credentials and generate a JWT token.

    Args:
        user_data: User data including username, email, profile image, and sub.

    Returns:
        A dictionary containing a JWT token or an error message.
    """
    users_collection = db["third_party_users"]

    existing_user = users_collection.find_one({'$or': [{'email': user_data.email}, {'sub': user_data.sub}]})

    if existing_user:
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
    


# Get user data by email from both 'users' and 'third_party_users' collections
async def get_user_data(email):

    users_collection = db["users"]
    user_data = users_collection.find_one({'email': email}, {"_id": 0, "password": 0})  # Exclude _id and password fields

    if user_data:
        return user_data

    # If not found in 'users', check in 'third_party_users'
    third_party_users_collection = db["third_party_users"]
    third_party_user_data = third_party_users_collection.find_one({'email': email}, {"_id": 0})

    return third_party_user_data

# generate the reset Token for the user request
async def generate_reset_token():
    reset_token = str(uuid.uuid4())
    timestamp = datetime.now().timestamp()
    return f"{reset_token}-{timestamp}"


async def update_request_token(email):
    token = await generate_reset_token()

    user_collection = db["users"]

    user_collection.update_one({"email":email},{"$set":{"reset_token":token}})

    return {"message":f"Update the token"}