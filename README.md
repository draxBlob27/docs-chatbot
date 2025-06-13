# Document Research & Theme Identification Chatbot

A full-stack AI-powered chatbot system that allows users to upload documents and ask natural language questions. The system extracts and cites answers from individual documents and synthesizes common themes across them.


## Live Demo

The project is deployed on **Google Cloud Platform** using Cloud Run:

- **Frontend** (Streamlit): [https://frontend-image-853989606321.us-central1.run.app](https://frontend-image-853989606321.us-central1.run.app)  
- **Backend** (FastAPI): [https://backend-image-853989606321.us-central1.run.app](https://backend-image-853989606321.us-central1.run.app)

## Features

### Document Handling
- Upload and store 75+ documents (PDF, scanned images, text)
- OCR support for scanned documents using ocrmypdf and pymupdf4llm
- Persistent vector database storage using ChromaDB

### Query & Citation
- Ask natural language questions
- Extract relevant answers from each document
- Cite document ID, page number, and paragraph/sentence
- Tabular display of results per document

### Theme Identification
- Automatically detect major themes from all document responses
- Generate concise, synthesized summaries
- Include citations supporting each theme

### User Interface
- Streamlit-based frontend
- Upload documents, ask questions, and view results
- Clear document table and theme visualization

## Project Structure
```

.
├── backend
│   ├── app
│   │   ├── api
│   │   │   ├── query.py
│   │   │   ├── theme.py
│   │   │   └── upload.py
│   │   ├── core
│   │   │   └── database.py
│   │   ├── main.py
│   │   ├── models
│   │   │   └── schema.py
│   │   └── services
│   │       ├── citation.py
│   │       ├── embedding.py
│   │       ├── parsing.py
│   │       ├── search.py
│   │       └── summarizer.py
│   ├── Dockerfile
│   ├── makefile
│   └── requirements.txt
├── demo
├── docker-compose.yml
├── docs
│   └── approach.md
├── frontend
│   ├── components
│   │   ├── document_table.py
│   │   ├── query_box.py
│   │   ├── theme_view.py
│   │   └── uploader.py
│   ├── Dockerfile
│   ├── makefile
│   ├── requirements.txt
│   └── streamlit_app.py
├── makefile
├── README.md
└── tests
    ├── test_api.py
    ├── test_parsing.py
    ├── test_search.py
    └── test_theme.py

```

## Tech Stack

- **Backend**: Python, FastAPI  
- **Frontend**: Streamlit  
- **OCR**: ocrmypdf, pymupdf4llm, pymupdf, spacy
- **LLM**: Groq  
- **Vector DB**: ChromaDB  
- **Testing**: Pytest  
- **Deployment**: Docker, Docker Compose, Google cloud

## Setup Instructions

1. **Clone the repo**
   ```bash
   git clone https://github.com/SanilParmar-wasserstoff-AiInternTask
   cd SanilParmar-wasserstoff-AiInternTask
