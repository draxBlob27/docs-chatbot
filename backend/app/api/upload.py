from fastapi import APIRouter, UploadFile, File
from backend.app.services.parsing import preprocess_document
from backend.app.services.embedding import embed_file
from backend.app.core.database import store_chunks
from backend.app.models.schema import UploadResponse
import os

router = APIRouter()

UPLOAD_DIR = "/Users/sanilparmar/Desktop/wasserStoff_chatbot/backend/data"

@router.post("/upload/", response_model=UploadResponse)
async def upload_and_process(file: UploadFile = File(...)):
    try:
        file_path = os.path.join(UPLOAD_DIR, file.filename)
        with open(file_path, "wb") as f:
            f.write(await file.read())

        chunks = preprocess_document(file_path)
        embedded_chunks = embed_file(chunks)
        store_chunks(chunks=chunks, embeddings=embedded_chunks)

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
