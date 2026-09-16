import os
import numpy as np
from app.services.embedder import embed

# Lazy Pinecone client
_pc = None
_index = None
_local_docs = None
_local_embeddings = None

def _get_pinecone_index():
    global _pc, _index
    api_key = os.getenv("PINECONE_API_KEY")
    index_name = os.getenv("PINECONE_INDEX")
    if not api_key or not index_name:
        return None
    if _index is None:
        try:
            from pinecone import Pinecone
            _pc = Pinecone(api_key=api_key)
            _index = _pc.Index(index_name)
        except Exception:
            _index = None
    return _index

def _get_local_kb():
    global _local_docs, _local_embeddings
    if _local_docs is None:
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        kb_path = os.path.join(base_dir, "data", "knowledge_base", "docs.txt")
        if os.path.exists(kb_path):
            with open(kb_path, "r", encoding="utf-8") as f:
                _local_docs = [line.strip() for line in f if line.strip()]
        else:
            _local_docs = [
                "Jarvis is an enterprise AI assistant designed to help employees quickly access internal company knowledge.",
                "Jarvis uses retrieval-augmented generation (RAG) to eliminate hallucinations and maintain accuracy.",
                "Security and data privacy are core principles. All data is processed within enterprise boundaries."
            ]
        _local_embeddings = [np.array(embed(doc)) for doc in _local_docs]
    return _local_docs, _local_embeddings

def retrieve(query: str, k: int = 3):
    """
    Retrieve top-k relevant documents from Pinecone (cloud) or local knowledge base (offline fallback)
    """
    index = _get_pinecone_index()
    vector = embed(query)

    if index is not None:
        try:
            results = index.query(
                vector=vector,
                top_k=k,
                include_metadata=True
            )
            return [
                match["metadata"]["text"]
                for match in results["matches"]
            ]
        except Exception:
            pass

    # Resilient local fallback using cosine similarity
    docs, doc_embeddings = _get_local_kb()
    q_vec = np.array(vector)
    norm_q = np.linalg.norm(q_vec)

    scores = []
    for doc, d_vec in zip(docs, doc_embeddings):
        norm_d = np.linalg.norm(d_vec)
        sim = float(np.dot(q_vec, d_vec) / (norm_q * norm_d)) if norm_q and norm_d else 0.0
        scores.append((sim, doc))

    scores.sort(key=lambda x: x[0], reverse=True)
    return [doc for _, doc in scores[:k]]
