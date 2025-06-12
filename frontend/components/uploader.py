'''
    Creates a file upload component in frontend. Allows multiple file to be selected at 
    once.
    Uses a HTTP POST request to upload file based on upload api call.
'''

import streamlit as st
import requests
import os

# If env var not uses localhost, used in cloud for connecting with backend
BASE_URL = os.getenv("API_URL", "http://localhost:8000")

ALLOWED_TYPES = [
    "pdf", "txt", "md",       # documents
    "jpg", "jpeg", "png",     # common image formats
    "tiff", "tif", "bmp"      # additional image formats
]


def uploader():
    st.header("Upload Documents")

    uploaded_files = st.file_uploader(
        "Choose one or more documents (PDF, Text, Images)",
        type=ALLOWED_TYPES,
        accept_multiple_files=True
    )

    if uploaded_files and st.button("Upload and Process"):
        for file in uploaded_files:
            st.write(f"Uploading {file.name}...")
            files = {'file': (file.name, file.getvalue(), file.type)}

            try:
                response = requests.post(f"{BASE_URL}/upload/", files=files)
                if response.status_code == 200:
                    result = response.json()
                    st.success(f"{file.name} uploaded. {result['chunks_stored']} chunks stored.")
                else:
                    st.error(f"Failed to upload {file.name}. Server error.")
            except Exception as e:
                st.error(f"Error: {e}")
