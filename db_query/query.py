from config.db import client
from passlib.hash import bcrypt 

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
    user_data.password = hashed_password  # Update the user_data object with the hashed password

    # go ahead and create the user
    user_id = users_collection.insert_one(user_data.dict()).inserted_id
    return {"user_id": str(user_id)}
