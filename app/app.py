from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api import api
from core.database import engine
from core.models import Base


load_dotenv()

# Initialize all database table
Base.metadata.create_all(bind=engine)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:9090"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTION"],
    allow_headers=["*"],
)

app.include_router(api.router)
