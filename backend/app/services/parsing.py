import spacy
from pymupdf4llm import LlamaMarkdownReader

nlp = spacy.load("en_core_web_md")

def extract_sentence_level_chunks(filepath: str):
    llama_reader = LlamaMarkdownReader()
    llama_docs = llama_reader.load_data(filepath)

    result = []

    for page in llama_docs:
        compTxt = page.text
        page_number = page.metadata['page']
        file_name = page.metadata['file_path']

        paragraphs = compTxt.split("\n\n")
        for i, paragraph in enumerate(paragraphs, 1):
            if paragraph.strip():
                doc = nlp(paragraph)
                sentences = doc.sents
                for j, sent in enumerate(sentences, 1):
                    metadataPage = {
                        'file_name': file_name,
                        'page_number': page_number,
                        'paragraph_number': i,
                        'sentence_number': j,
                    }
                    result.append({
                        "text": sent.text.strip(),
                        "metadata": metadataPage
                    })

    return result
