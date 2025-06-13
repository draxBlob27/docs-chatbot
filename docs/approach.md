# Approach & System Design

This document outlines the end-to-end architecture and implementation methodology for the Document Research & Theme Identification Chatbot.

## 1. Document Upload & Preprocessing

**Objective**: Allow users to upload documents → Extract text (including OCR for scanned files) → Store in a searchable format.

### Backend Components
- `upload.py`: FastAPI endpoint for uploading PDFs, scanned images, and text files.
- `parsing.py`: Uses ocrmypdf and pymupdf4llm to extract text from PDFs.
  #### Challenges:
  - **Diverse Formatting**: Some pdfs can be scanned, some can be text searchhable, images can have transparency.
  - **Inconsistent Text Encoding**: PDFs generated from various software can yield inconsistent Unicode or character spacing.
  - **ocrmypdf and pymupdf incompatibility**: `ocrmypdf` sometimes outputs glyphless or image-encoded text, which `pymupdf4llm` cannot parse. To handle this, PDFs were regenerated using `PyMuPDF` as an intermediate step before passing to `pymupdf4llm`.
- `embedding.py`: Converts extracted text into embeddings using SentenceTransformers.
- `database.py`: Stores metadata and vector embeddings in a vector database chromaDB.

### Frontend Components
- `uploader.py`: Streamlit component that lets users upload documents.

## 2. Question → Per-document Answer + Citation

**Objective**: User asks a question → Search relevant text chunks → Return answers from each document with proper citation.

### Backend Components
- `query.py`: API to receive a user question, perform semantic search, and return top-k chunks per document.
- `search.py`: Vector search logic implemented using chromaDB.
- `citation.py`: Parses file name, page, and paragraph from results and attaches it to the output.

### Frontend Components
- `query_box.py`: Streamlit component for entering user questions.
- `document_table.py`: Displays answers in a table format with columns for file name, extracted answer, and citation.

## 3. Theme Identification & Synthesis

**Objective**: Analyze all retrieved answers → Identify key themes → Generate chat-style synthesized summary with citations.

### Backend Components
- `theme.py`: Processes per-document answers for each user query.
- `summarizer.py`: Uses an LLM (LLaMA using GROQ) with a crafted prompt to generate high-level themes.
  
### Frontend Components
- `theme.py` : Generates response from LLM.

## 6. Internal Models & Schemas

- `backend/app/models/schema.py`: Defines Pydantic models for:
  - Request/response structures (e.g., query input, upload metadata)
  - Internal data formats passed between modules (e.g., parsed document structure, citation format)

## 5. Application Entry Points

- `backend/app/main.py`: Initializes and runs the FastAPI server, including all API routes from `api/`.
- `frontend/streamlit_app.py`: Entry point for launching the Streamlit interface and rendering all frontend components.

## 4. Infrastructure & Deployment

- Dockerfiles (`backend/Dockerfile`, `frontend/Dockerfile`) and `docker-compose.yml` are used to containerize and orchestrate the system.
- `makefile`: Defines standard commands for building, running, and testing the app.

## 5. Testing Strategy

- Unit tests exist under `tests/`, covering:
  - API behavior (`test_api.py`)
  - Text parsing logic (`test_parsing.py`)
  - Search and retrieval (`test_search.py`)
  - Theme generation (`test_theme.py`)


