# Creates fastapi app

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import upload, query, theme

app = FastAPI(
    title="Wasserstoff Document QA Backend",
    description="Upload documents, run semantic search, extract themes with citations.",
    version="1.0.0"
)

# CORS for allowing frontend(external service) to connect with backend, when browser stops doing it so.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], #Allows requests from all origins.
    allow_credentials=True, 
    allow_methods=["*"], #Allows all HTTP methods(GET, POST,...)
    allow_headers=["*"],
)

# Enables router capabilty
app.include_router(upload.router)
app.include_router(query.router)
app.include_router(theme.router)

@app.get("/")
async def root():
    return {"message": "Backend is running. Visit /docs to test."} #Default message at root.
