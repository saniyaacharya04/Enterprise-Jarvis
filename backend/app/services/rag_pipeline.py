from app.services.retriever import retrieve
from app.services.llm_service import generate

def run_rag(query: str):
    context_docs = retrieve(query)
    context = "\n".join(context_docs)

    prompt = f"""
You are an enterprise AI assistant.
Answer using ONLY the context below.

Context:
{context}

Question:
{query}
"""

    return generate(prompt)
