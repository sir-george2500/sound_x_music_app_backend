from fastapi import FastAPI ,HTTPException
import uvicorn
from fastapi.middleware.cors import CORSMiddleware
from config.db import client
app = FastAPI()

app = FastAPI(
    description="Test out your Api Route",
    title="SoundX Backend",
    docs_url="/"
)

# Configure CORS middleware
origins = [
    "http://localhost:3000",
    # Add more allowed origins if needed
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/test_db_connection")
def test_db_connection():
    try:
        db = client["sound-x"]
        collection = db["users"]
        document = collection.find_one()
        return {"message": "Database connection successful!"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error connecting to database: {str(e)}")

    if __name__ == '__main__':
      uvicorn.run("main:app", reload=True)