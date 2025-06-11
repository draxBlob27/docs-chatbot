from fastapi import FastAPI, UploadFile, File
import os

UPLOAD_DIR = "/Users/sanilparmar/Desktop/wasserStoff_chatbot/backend/data"

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "go to http://127.0.0.1:8000/docs!"}

@app.post("/uploadFile/")
async def upload_file(file: UploadFile = File()):
    file_location = os.path.join(UPLOAD_DIR, file.filename)
    with open (file_location, "wb") as f:
        f.write(file.read())
    print(f"filename: {file.filename}, content_type: {file.content_type}, Saved succesfully at: {file_location}")