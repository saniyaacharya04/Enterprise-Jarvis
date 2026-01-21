from sentence_transformers import SentenceTransformer

# Load embedding model once at startup
_model = SentenceTransformer("all-MiniLM-L6-v2")

def embed(text: str):
    """
    Convert text into a vector embedding
    """
    return _model.encode(text).tolist()
