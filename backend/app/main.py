from fastapi import FastAPI
from dotenv import load_dotenv
import os

# Load environment variables from .env at backend startup
load_dotenv()

from app.api.chat import router as chat_router

app = FastAPI(title="Enterprise Jarvis")

app.include_router(chat_router, prefix="/api")