import streamlit as st
from components.uploader import uploader
from components.query_box import query_box
from components.document_table import document_table
from components.theme_view import theme_view

st.set_page_config(
    page_title="Document QA",
    layout="wide"
)

st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["Upload Documents", "Ask a Question", "Summarize Themes"])

if page == "Upload Documents":
    st.title("Upload Your Documents")
    uploader()

elif page == "Ask a Question":
    st.title("Ask a Question")
    results = query_box()
    document_table(results)

elif page == "Summarize Themes":
    st.title("Theme Summarization")
    theme_view()
