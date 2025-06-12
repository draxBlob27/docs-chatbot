import streamlit as st
import requests
import os

BASE_URL = os.getenv("API_URL", "http://localhost:8000")

def query_box(query=None, top_k=5):
    if not query:
        st.warning("No query provided.")
        return []

    results = []
    with st.spinner("Searching..."):
        try:
            response = requests.get(f"{BASE_URL}/query/", params={"q": query, "top_k": top_k})
            if response.status_code == 200:
                results = response.json()
            else:
                st.error("Search failed.")
        except Exception as e:
            st.error(f"Error: {e}")
    return results
