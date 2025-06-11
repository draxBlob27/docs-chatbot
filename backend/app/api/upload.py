from fastapi import APIRouter, UploadFile, File
from backend.app.services.parsing import preprocess_document
from backend.app.services.embedding import embed_and_store
from backend.app.services.search import search
import os

router = APIRouter()

UPLOAD_DIR = "/Users/sanilparmar/Desktop/wasserStoff_chatbot/backend/data"

@router.post("/upload/")
async def upload_and_process(file: UploadFile = File(...)):
    try:
        file_path = os.path.join(UPLOAD_DIR, file.filename)
        with open(file_path, "wb") as f:
            f.write(await file.read())

        chunks = preprocess_document(file_path)
        embed_and_store(chunks)

        return {
            "filename": file.filename,
            "chunks_stored": len(chunks),
            "message": "File uploaded, parsed, and embedded successfully.",
        }

    except Exception as e:
        return {
            "error": str(e),
            "message": "An error occurred during upload or processing.",
        }

@router.get("/search/")
async def search_docs(query: str, top_k: int = 5):
    try:
        results = search(query, top_k)
        return {"results": results}
    except Exception as e:
        return {
            "error": str(e),
            "message": "An error occurred during search.",
        }
