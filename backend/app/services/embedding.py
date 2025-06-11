import uuid
from typing import List, Dict
import chromadb
from sentence_transformers import SentenceTransformer
from backend.app.core.database import collection

model = SentenceTransformer("all-MiniLM-L6-v2")

def embed_and_store(chunks: List[Dict]):
    for i, chunk in enumerate(chunks):
        text = chunk["text"]
        metadata = chunk["metadata"]
        doc_id = metadata.get("file_name", "unknown").split("/")[-1]
        uid = f"{doc_id}_{i}_{uuid.uuid4().hex[:8]}"

        embedding = model.encode(text).tolist()

        collection.upsert(
            documents=[text],
            embeddings=[embedding],
            metadatas=[metadata],
            ids=[uid]
        )



