from fastapi import FastAPI ,HTTPException
import uvicorn
from routes import router 
from fastapi.middleware.cors import CORSMiddleware

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


    

app.include_router(router, tags=["routes"],prefix="/sound-x")
if __name__ == '__main__':
      uvicorn.run("main:app", reload=True)