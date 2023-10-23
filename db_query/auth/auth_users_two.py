# Import necessary modules and libraries
from config.db import client
from datetime import datetime, timedelta
from config.db import client
from passlib.hash import bcrypt 

#db client
db = client["sound-x"]



def validate_token(collection, delimiter=0, **kwargs):
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




