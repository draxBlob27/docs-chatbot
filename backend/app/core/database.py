import chromadb

CHROMA_DB_PATH = "/Users/sanilparmar/Desktop/wasserStoff_chatbot/backend/data/vectordb"

chroma_client = chromadb.PersistentClient(path=CHROMA_DB_PATH)
collection = chroma_client.get_or_create_collection(name="document_chunks")
