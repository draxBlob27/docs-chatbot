from typing import Dict

def extract_citation(metadata: Dict) -> str:
    file_name = metadata.get("file_name", "UnknownFile")
    page = metadata.get("page_number")
    para = metadata.get("paragraph_number")
    sentence = metadata.get("sentence_number")

    citation_parts = [file_name]

    if page is not None:
        citation_parts.append(f"Page {page}")
    if para is not None:
        citation_parts.append(f"Para {para}")
    if sentence is not None:
        citation_parts.append(f"Sentence {sentence}")

    return " – ".join(citation_parts)


def attach_citation_to_result(result_chunk: Dict) -> Dict:
    return {
        "text": result_chunk.get("text", ""),
        "citation": extract_citation(result_chunk.get("metadata", {}))
    }
