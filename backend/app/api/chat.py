from fastapi import APIRouter
from app.models.chat_schema import ChatRequest
from app.services.rag_pipeline import run_rag

router = APIRouter()

@router.post("/chat")
def chat(request: ChatRequest):
    query = request.query.lower()

    # ⚡ Fast identity handling (no retrieval needed)
    if "your name" in query or "who are you" in query:
        return {
            "response": "I am Enterprise Jarvis, your AI assistant for secure internal knowledge."
        }

    # Normal RAG flow
    answer = run_rag(request.query)
    return {"response": answer}
