from fastapi import FastAPI
from dotenv import load_dotenv
import os

# Load environment variables from .env at backend startup
load_dotenv()

from app.api.chat import router as chat_router

app = FastAPI(
    title="Enterprise Jarvis",
    description="Enterprise RAG knowledge assistant with secure vector retrieval",
    version="1.0.0"
)

@app.get("/health")
def health_check():
    return {"status": "healthy", "service": "Enterprise Jarvis", "version": "1.0.0"}

app.include_router(chat_router, prefix="/api")