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
page = st.sidebar.radio("Go to", ["Upload Documents", "Ask & Summarize"])

if page == "Upload Documents":
    uploader()

elif page == "Ask & Summarize":
    st.title("Ask a Question & Summarize Themes")
    query = st.text_input("Enter your question about the documents:")
    top_k = st.slider("Number of results", min_value=1, max_value=30, value=5)

    if query and st.button("Run Query and Theme Summary"):
        results = query_box(query=query, top_k=top_k)
        document_table(results)

        st.divider()
        st.subheader("Themes based on query")
        theme_view(query=query, top_k=top_k)
