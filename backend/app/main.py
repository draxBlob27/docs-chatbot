from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.app.api import upload 

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(upload.router)

@app.get("/")
async def root():
    return {"message": "Backend is running. Visit /docs to interact."}
