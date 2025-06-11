FROM python:3.11-slim

WORKDIR /app

RUN apk add --no-cache \
    poppler-utils \
    tesseract-ocr \
    ghostscript \
    gcc \
    musl-dev \
    linux-headers

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000
CMD ["uvicorn", "backend.app.main:app", "--host", "0.0.0.0", "--port", "8000"]