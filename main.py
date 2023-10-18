from fastapi import FastAPI 
import uvicorn
from routes.audio_routes import audio_router
from routes.auth_routes  import auth_router
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


    

app.include_router(auth_router, tags=["Users Authentication Routes"],prefix="/sound-x")
app.include_router(audio_router, tags=["Audio Routes"],prefix="/sound-x")
if __name__ == '__main__':
      uvicorn.run("main:app", reload=True)