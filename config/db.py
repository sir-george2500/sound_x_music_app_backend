from pymongo import MongoClient
from dotenv  import load_dotenv
import os

# Load environment variables from .env
load_dotenv()

database_url = os.getenv("DATABASE_URL")

client = MongoClient(database_url)
