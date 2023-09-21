from config.db import client

#test if the database is connected
def testconnection():
        db = client["sound-x"]
        collection = db["users"]
        document = collection.find_one()
        return {"message": "Database connection successful!"}

#create the user
def create_user(user_data):
        db = client["sound-x"]
        users_collection = db["users"]

        #check if the user exist in the DB
        if users_collection.find_one({'$or': [{'email': user_data.username}, {'email': user_data.email}]}):
            return {"error": "Username or email already exists"}
        
        #then go ahead and create the user
        user_id = users_collection.insert_one(user_data.dict()).inserted_id
        return {"user_id": str(user_id)}


   

