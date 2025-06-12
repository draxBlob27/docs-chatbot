# Python image
FROM python:3.11-slim 

# Directory where main.py(in my case) is (/backend -> Dockerfile, /backend/app -> main)
WORKDIR /app

# install dependancies
RUN apt-get update && apt-get install -y \
    poppler-utils \
    tesseract-ocr \
    ghostscript \
    gcc \
    g++ \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# install pips
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# copy whole directory
COPY . .

# exposes port 8080, default for cloud deployment, locally at port 8000
EXPOSE 8080

# command to run backend
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080"]

