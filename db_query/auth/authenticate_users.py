# Import necessary modules and libraries
from config.db import client
from passlib.hash import bcrypt 
from datetime import datetime, timedelta
from dotenv  import load_dotenv
import os
import jwt
from datetime import datetime, timedelta
import random
import smtplib
from email.message import EmailMessage

# Load environment variables from .env
load_dotenv()

# Global variables for secret key and algorithm
SECRET_KEY = os.getenv("SECRET_KEY") 
SECRET_EMAIL = os.getenv("SECRET_EMAIL")
SECRET_PASSWORD = os.getenv("SECRET_EMAIL_PASSWORD")
ALGORITHM = "HS256"


#db client
db = client["sound-x"]

# variadic  function for checking in the Database for user
def check_in_db(collection, delimiter=2, **kwargs):
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

    if delimiter == 1:
        # Construct a query with multiple conditions (AND)
        query = {field: value for field, value in kwargs.items()}
    elif delimiter == 2:
        # Construct a query with multiple conditions (OR)
        or_conditions = [{field: value} for field, value in kwargs.items()]
        query = {'$or': or_conditions}
    else:
        raise ValueError("Invalid delimiter value. Use 1 for AND or 2 for OR.")

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
    """Gets the user data for the given email address.

    Args:
        email: The email address of the user.

    Returns:
        A dictionary containing the user data, or None if the user is not found.
    """

    users_collection = db["users"]
    user_data = users_collection.find_one({'email': email}, {"_id": 0, "password": 0})  # Exclude _id and password fields

    if user_data:
        return user_data

    # If not found in 'users', check in 'third_party_users'
    third_party_users_collection = db["third_party_users"]
    third_party_user_data = third_party_users_collection.find_one({'email': email}, {"_id": 0})

    return third_party_user_data


async def generate_reset_token():
    """Generates a random reset token.

    Returns:
        A string containing the reset token.
    """

    reset_token = str(random.randint(100000, 999999))
    return f"{reset_token}"


async def update_request_token(email):
    """Updates the reset token for the given email address.

    Args:
        email: The email address of the user.

    Returns:
        The reset token.
    """

    token = await generate_reset_token()

    # Calculate expiry time (1 hour from now)
    expiry_time = datetime.now() + timedelta(hours=1)

    user_collection = db["users"]

    user_collection.update_one(
        {"email": email},
        {
            "$set": {
                "reset_token": token,
                "token_expiry": expiry_time
            }
        }
    )
    return token


async def send_reset_password_email(useremail, token):
    """Sends an email to the user with a link to reset their password.

    Args:
        email: The user's email address.
        token: The reset token.
    """

    HOST = "smtp-mail.outlook.com"
    PORT = 587


    msg = EmailMessage()
    msg['Subject'] = "Reset your password on Sound-X"
    msg['From'] = "soundX.app@outlook.com"
    msg['To'] = useremail

    msg.set_content(f"Hi there,\n\nHere is your reset code to reset your password on Sound-X: {token}\n\nThis code is valid for 1 hour.\n\nThanks,\nThe Sound-X Team")

    smtp = smtplib.SMTP(HOST, PORT)
    smtp.starttls()
    
    #print(PASSWORD)
    smtp.login(SECRET_EMAIL, SECRET_PASSWORD)
    smtp.sendmail(msg['From'], msg['To'], msg.as_string())
    smtp.quit()

    return {"message": "Email sent"}

