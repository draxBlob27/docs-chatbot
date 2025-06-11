import streamlit as st
import requests
import os

BASE_URL = os.getenv("API_URL", "http://localhost:8000")

def theme_view():
    st.header("Theme Summarizer")

    query = st.text_input("Ask a question to summarize across documents:")
    top_k = st.slider("Number of results", 1, 30, 5)

    if query and st.button("Summarize Themes"):
        with st.spinner("Generating themes..."):
            try:
                response = requests.get(f"{BASE_URL}/theme/", params={"q": query, "top_k": top_k})
                if response.status_code == 200:
                    themes = response.json()
                    for theme in themes:
                        st.markdown(f"### {theme['theme']}")
                        st.markdown(f"{theme['summary']}")
                        with st.expander("Citations"):
                            for cite in theme["citations"]:
                                st.markdown(f"- {cite}")
                else:
                    st.error("Theme generation failed.")
            except Exception as e:
                st.error(f"Error: {e}")
