
FROM python:3.11-slim


RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    rustc \
    ffmpeg \
    portaudio19-dev \
    libxml2-dev \
    libxslt-dev \
    libjpeg-dev \
    zlib1g-dev \
    libfreetype6-dev \
    liblcms2-dev \
 && rm -rf /var/lib/apt/lists/*



WORKDIR /app


COPY requirements.txt .

COPY . .



RUN pip install --no-cache-dir --upgrade pip setuptools wheel
RUN pip install --no-cache-dir -r requirements.txt


COPY . .

ENV ASANA_ACCESS_TOKEN=2/1203963127593922/1209079337408326:d93bdf5bd31a37f50e67c694aa956465


EXPOSE 8000


CMD ["python", "main.py"]
