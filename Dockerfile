# Debian slim image'ından türet
FROM debian:bullseye-slim

# Gerekli paketleri kur: Python, pip ve tesseract
RUN apt-get update && apt-get install -y --no-install-recommends \
    python3 \
    python3-pip \
    tesseract-ocr \
    tesseract-ocr-eng \
    ffmpeg libsm6 libxext6 \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

RUN python3 --version
RUN which python3

COPY requirements.txt .
RUN pip3 install -r requirements.txt

COPY app.py .
COPY captcha_solver.py .

EXPOSE 8000

CMD python3 -m uvicorn app:app --host=0.0.0.0 --port=8000