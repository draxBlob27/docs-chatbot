import streamlit as st
import requests
import os

BASE_URL = os.getenv("API_URL", "http://localhost:8000")

def query_box():
    st.header("Ask a Question")

    query = st.text_input("Enter your question about the documents:")
    top_k = st.slider("Number of results", min_value=1, max_value=30, value=5)

    results = []
    if query and st.button("Search"):
        with st.spinner("Searching..."):
            try:
                response = requests.get(f"{BASE_URL}/query/", params={"q": query, "top_k": top_k})
                if response.status_code == 200:
                    results = response.json()
                else:
                    st.error("Search failed. Check backend logs.")
            except Exception as e:
                st.error(f"Error: {e}")
    
    return results
