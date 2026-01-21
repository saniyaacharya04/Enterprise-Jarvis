import os
from pinecone import Pinecone
from app.services.embedder import embed

# Initialize Pinecone client
pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))

index_name = os.getenv("PINECONE_INDEX")

index = pc.Index(index_name)

def retrieve(query: str, k: int = 3):
    """
    Retrieve top-k relevant documents from Pinecone
    """
    vector = embed(query)

    results = index.query(
        vector=vector,
        top_k=k,
        include_metadata=True
    )

    return [
        match["metadata"]["text"]
        for match in results["matches"]
    ]
