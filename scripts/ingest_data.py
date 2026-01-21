import sys
import os
from dotenv import load_dotenv
from pinecone import Pinecone, ServerlessSpec

# -------------------------------
# Setup
# -------------------------------
load_dotenv()

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
BACKEND_PATH = os.path.join(PROJECT_ROOT, "backend")
sys.path.insert(0, BACKEND_PATH)

from app.services.embedder import embed

# -------------------------------
# Pinecone init
# -------------------------------
pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))

INDEX_NAME = os.getenv("PINECONE_INDEX")
DIMENSION = 384  # all-MiniLM-L6-v2

# Create index if missing
if INDEX_NAME not in pc.list_indexes().names():
    pc.create_index(
        name=INDEX_NAME,
        dimension=DIMENSION,
        metric="cosine",
        spec=ServerlessSpec(
            cloud="aws",
            region="us-east-1"
        )
    )
    print(f"🆕 Created index: {INDEX_NAME}")

index = pc.Index(INDEX_NAME)

# -------------------------------
# Load & clean documents
# -------------------------------
with open("backend/app/data/knowledge_base/docs.txt") as f:
    texts = [line.strip() for line in f if line.strip()]

print(f"Loaded {len(texts)} non-empty documents")

# -------------------------------
# Build vectors safely
# -------------------------------
vectors = []

for i, text in enumerate(texts):
    embedding = embed(text)

    # Safety check (CRITICAL)
    if len(embedding) != DIMENSION:
        print(f"Skipping doc {i}: invalid embedding size {len(embedding)}")
        continue

    vectors.append({
        "id": str(i),
        "values": embedding,
        "metadata": {"text": text}
    })

print(f"Prepared {len(vectors)} vectors")

# -------------------------------
# Upsert in small batches
# -------------------------------
BATCH_SIZE = 50

for i in range(0, len(vectors), BATCH_SIZE):
    batch = vectors[i:i + BATCH_SIZE]
    index.upsert(vectors=batch)

print("Knowledge ingested into Pinecone successfully")
import time
time.sleep(2)
print("Knowledge ingested into Pinecone successfully")
