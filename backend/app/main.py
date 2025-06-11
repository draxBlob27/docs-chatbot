from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.app.api import upload, query, theme

app = FastAPI(
    title="Wasserstoff Document QA Backend",
    description="Upload documents, run semantic search, extract themes with citations.",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(upload.router)
app.include_router(query.router)
app.include_router(theme.router)

@app.get("/")
async def root():
    return {"message": "Backend is running. Visit /docs to test."}
