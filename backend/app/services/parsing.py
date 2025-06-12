'''
    Performs ocr based text extraction for scanned pdf and images, othrewise for text pdf
    performs text extraction and return list of chunks with metadata based on sentences 
    using spacy.
'''
import os
import spacy #Module for paragraph and sentence citation. Uses english models
import ocrmypdf #On scanned pdfs add a layer of text to convert it to text pdf.
import pymupdf #Here used for helping pymupdf4llm with ocrmypdf output
from typing import List, Dict 
from pathlib import Path
from pymupdf4llm import LlamaMarkdownReader 
from PIL import Image

# Natural language parser sm(small) core english model
nlp = spacy.load("en_core_web_sm")

'''
    This functions checks if pdf is text searchable or scanned.
'''
def is_pdf_text_based(pdf_path: str) -> bool:
    try:
        llama_reader = LlamaMarkdownReader()
        docs = llama_reader.load_data(pdf_path)
        total_chars = 0
        pages_to_check = min(3, len(docs))
        for i, page in enumerate(docs):
            if i >= pages_to_check:
                break
            text = page.text.strip()
            total_chars += len(text)
        return total_chars > 100
    except Exception:
        return False

'''
    Fixes ocrmypdf output, which was incompatible with pymupdf4llm.
    ocrmypdf output is compatible with pymupdf, this func creates
    new pdf compatible with pymupdf4llm.
    Incomptabilty occured due to glyphless font layer added by ocrmypdf.
'''
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

'''
    For images input with alpha(i.e. transparency), removes alpha and return new image which is
    RGB.
'''
def preprocess_image(input_path: str) -> str:
    try:
        with Image.open(input_path) as img:
            if img.mode in ('RGBA', 'LA'):
                rgb_img = Image.new('RGB', img.size, (255, 255, 255))
                if img.mode == 'RGBA':
                    rgb_img.paste(img, mask=img.split()[-1])
                else:
                    rgb_img.paste(img.convert('RGB'))
                processed_path = str(Path(input_path).with_name(Path(input_path).stem + "_processed.png"))
                rgb_img.save(processed_path, 'PNG')
                return processed_path
            else:
                return input_path
    except Exception:
        return input_path

'''
    Parses scanned pdf and images, by ocrmypdf, which creates a new pdf with text layer.
'''
def run_ocr_and_return_pdf(input_path: str) -> str:
    ext = Path(input_path).suffix.lower()
    output_path = str(Path(input_path).with_name(Path(input_path).stem + "_ocr.pdf"))
    fixed_output_path = str(Path(input_path).with_name(Path(input_path).stem + "_fixed.pdf"))

    if ext in [".jpg", ".jpeg", ".png", ".tiff", ".tif", ".bmp"]:
        processed_input = preprocess_image(input_path)
        ocrmypdf.ocr(
            processed_input, 
            output_path, 
            language="eng",
            image_dpi=300 #Most parsing softwares handles 300 dpi best. (600 -> Big size, 100 -> Low quality)
        )
        return fix_glyphless_font_pdf(output_path, fixed_output_path)
    elif ext == ".pdf":
        #For documents with digital signature ocrmypdf fails as it will invalidate siganture. 
        ocrmypdf.ocr(input_path, output_path, language="eng", force_ocr=True, invalidate_digital_signatures=True)
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
                doc = nlp(paragraph) #Based on logic of nlp model, separates sentences from paragraphs.
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

#If text file or markdown files directly runs pymupdf4llm to extract chunks.
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
    elif ext in [".jpg", ".jpeg", ".png", ".tiff", ".tif", ".bmp"]: #added extra exts for safety
        searchable_pdf = run_ocr_and_return_pdf(filepath)
        return chunk_pdf(searchable_pdf)
    elif ext == ".pdf":
        if is_pdf_text_based(filepath):
            try:
                return chunk_pdf(filepath)
            except Exception:
                searchable_pdf = run_ocr_and_return_pdf(filepath)
                return chunk_pdf(searchable_pdf)
        else:
            searchable_pdf = run_ocr_and_return_pdf(filepath)
            return chunk_pdf(searchable_pdf)
    else:
        raise ValueError(f"Unsupported file type: {ext}")

# Testing, uses dunder method ensuring not triggerring when called outside this script.
if __name__ == "__main__":
    import sys
    import json

    if len(sys.argv) < 2:
        print("Usage:")
        print("  python3 parsing.py path")
        sys.exit(1)

    try:
        input_path = sys.argv[1]
        if not Path(input_path).exists():
            print(f"Error: File not found: {input_path}")
            sys.exit(1)
        
        print(f"Processing document: {input_path}")
        chunks = preprocess_document(input_path)
        print(f"Extracted {len(chunks)} chunks")
        print("chunks preview:")
        #Initial 3 chunks to be displayed.
        for i, chunk in enumerate(chunks[:3]):
            print(f"\n{i+1}:")
            print(json.dumps(chunk, indent=2))
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)
