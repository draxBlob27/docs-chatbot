import os
import spacy
import ocrmypdf
import pymupdf
from typing import List, Dict
from pathlib import Path
from pymupdf4llm import LlamaMarkdownReader

nlp = spacy.load("en_core_web_sm")


def fix_glyphless_font_pdf(input_path: str, output_path: str) -> str:
    with pymupdf.open(input_path) as doc:
        with pymupdf.open() as new_doc:
            for page_num in range(len(doc)):
                page = doc[page_num]
                rect = page.rect
                new_page = new_doc.new_page(width=rect.width, height=rect.height)
                text_dict = page.get_text("dict")
                
                for block in text_dict.get("blocks", []):
                    if block.get("type") == 0:
                        for line in block.get("lines", []):
                            for span in line.get("spans", []):
                                text = span.get("text", "").strip()
                                if text:
                                    bbox = span["bbox"]
                                    font_size = span.get("size", 12)
                                    
                                    new_page.insert_text(
                                        (bbox[0], bbox[1]),
                                        text,
                                        fontname="helv", 
                                        fontsize=font_size,
                                        color=(0, 0, 0)
                                    )
            
            new_doc.save(output_path)
    return output_path


def run_ocr_and_return_pdf(input_path: str) -> str:
    ext = Path(input_path).suffix.lower()
    output_path = str(Path(input_path).with_name(Path(input_path).stem + "_ocr.pdf"))
    fixed_output_path = str(Path(input_path).with_name(Path(input_path).stem + ".pdf"))

    if ext in [".jpg", ".jpeg", ".png", ".tiff", ".tif", ".bmp"]:
        ocrmypdf.ocr(input_path, output_path, language="eng")
        return fix_glyphless_font_pdf(output_path, fixed_output_path)

    elif ext == ".pdf":
        ocrmypdf.ocr(input_path, output_path, language="eng", force_ocr=True)
        return fix_glyphless_font_pdf(output_path, fixed_output_path)

    else:
        raise ValueError(f"Unsupported file: {ext}")


def chunk_pdf(filepath: str) -> List[Dict]:
    llama_reader = LlamaMarkdownReader()
    docs = llama_reader.load_data(filepath)

    result = []

    for page in docs:
        compTxt = page.text
        page_number = page.metadata['page']
        file_name = page.metadata['file_path']

        paragraphs = compTxt.split("\n\n")
        for para_num, paragraph in enumerate(paragraphs, start=1):
            if paragraph.strip():
                doc = nlp(paragraph)
                sentences = doc.sents
                for sent_num, sent in enumerate(sentences, 1):
                    metadataPage = {
                        'file_name': file_name,
                        'page_number': page_number,
                        'paragraph_number': para_num,
                        'sentence_number': sent_num,
                    }
                    result.append({
                        "text": sent.text.strip(),
                        "metadata": metadataPage
                    })

    return result


def chunk_txt(filepath: str) -> List[Dict]:
    with open(filepath, "r") as file:
        content = file.read()

    paragraphs = content.split("\n\n")
    result = []

    for para_num, paragraph in enumerate(paragraphs, 1):
        if paragraph.strip():
            doc = nlp(paragraph)
            for sent_num, sent in enumerate(doc.sents, 1):
                result.append({
                    "text": sent.text.strip(),
                    "metadata": {
                        "file_name": Path(filepath).name,
                        "page_number": None,
                        "paragraph_number": para_num,
                        "sentence_number": sent_num,
                    }
                })

    return result


def preprocess_document(filepath: str) -> List[Dict]:
    ext = Path(filepath).suffix.lower()

    if ext in [".txt", ".md"]:
        return chunk_txt(filepath)

    elif ext in [".pdf", ".jpg", ".jpeg", ".png", ".tiff", ".tif", ".bmp"]:
        searchable_pdf = run_ocr_and_return_pdf(filepath)
        return chunk_pdf(searchable_pdf)

    else:
        raise ValueError(f"Unsupported file type: {ext}")

if __name__ == "__main__":
    import sys
    import json

    if len(sys.argv) < 2:
        print("Usage:")
        print("  python3 parsing.py path/to/document")
        sys.exit(1)

    try:
        input_path = sys.argv[1]
        if not Path(input_path).exists():
            print(f"Error: File not found: {input_path}")
            sys.exit(1)
        
        print(f"Processing document: {input_path}")
        chunks = preprocess_document(input_path)
        print(f"Extracted {len(chunks)} chunks")
        
        print("First few chunks preview:")
        for i, chunk in enumerate(chunks[:3]):
            print(f"\nChunk {i+1}:")
            print(json.dumps(chunk, indent=2, ensure_ascii=False))
                
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)