# Import necessary modules and libraries
from config.db import client
from datetime import datetime, timedelta
from config.db import client
from passlib.hash import bcrypt 

#db client
db = client["sound-x"]



async def validate_token(token):
    current_time = datetime.utcnow()

    collection = db['users']
    user = collection.find_one({"reset_token": token, "token_expiry": {"$gte": current_time}})
    if user:
        return user
    else:
        return None



