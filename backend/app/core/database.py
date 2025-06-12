'''
    Creates vector database to store vector embeddings of chunks and queries as well.
'''
import uuid
from typing import List, Dict
import chromadb

CHROMA_DB_PATH = "/Users/sanilparmar/Desktop/wasserStoff_chatbot/backend/data/vectordb"
chroma_client = chromadb.PersistentClient(path=CHROMA_DB_PATH)  #Persistent client for preventing shutting as soon as we leave service.
collection = chroma_client.get_or_create_collection(name="document_chunks") #Safety check to prevent name conflicts

def store_chunks(chunks: List[Dict], embeddings: List[List[float]]):
    for i, (chunk, embedding) in enumerate(zip(chunks, embeddings)):
        text = chunk["text"]
        metadata = chunk["metadata"]
        doc_id = metadata.get("file_name", "unknown").split("/")[-1]
        uid = f"{doc_id}_{i}_{uuid.uuid4().hex[:8]}"

        # Safety check to prevent same data being uploaded again
        collection.upsert(
            documents=[text],
            embeddings=[embedding],
            metadatas=[metadata],
            ids=[uid]
        )
