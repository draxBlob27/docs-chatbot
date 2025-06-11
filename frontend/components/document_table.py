import streamlit as st
from typing import List, Dict

def document_table(results: List[Dict]):
    if not results:
        st.info("No results to display.")
        return

    st.subheader("Search Results")

    table_data = []
    for res in results:
        citation = res["Citations"]
        text = res["Text"]
        file_name = citation.split("–")[0].strip() if "–" in citation else "Unknown"
        
        table_data.append({
            "Document": file_name,
            "Answer": text,
            "Citation": citation
        })

    st.table(table_data)
