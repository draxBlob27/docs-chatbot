import streamlit as st
from typing import List, Dict
import os

def document_table(results: List[Dict]):
    if not results:
        st.info("No results to display.")
        return

    st.subheader("Search Results")

    table_data = []
    for res in results:
        citation = res.get("citation", "N/A")
        text = res.get("text", "N/A")
        parts = citation.split("–", 1)
        full_path = parts[0].strip()
        remaining_citation = parts[1].strip()
        file_name = os.path.basename(full_path)
        
        table_data.append({
            "Document": file_name,
            "Answer": text,
            "Citation": remaining_citation
        })

    st.table(table_data)
