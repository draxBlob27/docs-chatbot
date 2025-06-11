import uuid
from typing import List, Dict


import chromadb
from sentence_transformers import SentenceTransformer

model = SentenceTransformer("all-MiniLM-L6-v2")

chroma_client = chromadb.PersistentClient(path = "/Users/sanilparmar/Desktop/wasserStoff_chatbot/backend/data/vectordb")

collection = chroma_client.get_or_create_collection(name="document_chunks")


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



