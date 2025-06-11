from backend.app.services.parsing import preprocess_document
import os

def test_parse_txt_sample():
    file_path = "backend/data/sample_1_ocr.pdf"
    chunks = preprocess_document(file_path)
    assert isinstance(chunks, list)
    assert all("text" in c and "metadata" in c for c in chunks)
    assert chunks[0]["metadata"].get("paragraph_number") == 1
