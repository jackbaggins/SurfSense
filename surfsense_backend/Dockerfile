FROM python:3.12-slim

WORKDIR /app

# Install system dependencies including SSL tools, CUDA dependencies, and Tesseract OCR
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    python3-dev \
    ca-certificates \
    curl \
    wget \
    unzip \
    gnupg2 \
    espeak-ng \
    libsndfile1 \
    libgl1 \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender1 \
    && rm -rf /var/lib/apt/lists/*

# Update certificates and install SSL tools
RUN update-ca-certificates
RUN pip install --upgrade certifi pip-system-certs
RUN pip install --no-cache-dir torch torchvision torchaudio

# Copy requirements
COPY pyproject.toml .
COPY uv.lock .

# Install python dependencies
RUN pip install --no-cache-dir uv && \
    uv pip install --system --no-cache-dir -e .

# Set SSL environment variables dynamically
RUN CERTIFI_PATH=$(python -c "import certifi; print(certifi.where())") && \
    echo "Setting SSL_CERT_FILE to $CERTIFI_PATH" && \
    echo "export SSL_CERT_FILE=$CERTIFI_PATH" >> /root/.bashrc && \
    echo "export REQUESTS_CA_BUNDLE=$CERTIFI_PATH" >> /root/.bashrc
ENV SSL_CERT_FILE=/usr/local/lib/python3.12/site-packages/certifi/cacert.pem
ENV REQUESTS_CA_BUNDLE=/usr/local/lib/python3.12/site-packages/certifi/cacert.pem

# Pre-download EasyOCR models to avoid runtime SSL issues
# RUN mkdir -p /root/.EasyOCR/model
# RUN wget --no-check-certificate https://github.com/JaidedAI/EasyOCR/releases/download/v1.3/english_g2.zip -O /root/.EasyOCR/model/english_g2.zip || true
# RUN wget --no-check-certificate https://github.com/JaidedAI/EasyOCR/releases/download/pre-v1.1.6/craft_mlt_25k.zip -O /root/.EasyOCR/model/craft_mlt_25k.zip || true
# RUN cd /root/.EasyOCR/model && (unzip -o english_g2.zip || true) && (unzip -o craft_mlt_25k.zip || true)

RUN pip install docling
# RUN docling-tools models download -o /opt/docling_models

# Pre-download Docling models
# RUN python -c "try:\n    from docling.document_converter import DocumentConverter\n    conv = DocumentConverter()\nexcept:\n    pass" || true

# Install Playwright browsers for web scraping if needed
RUN pip install playwright && \
    playwright install chromium

# Set a cache dir for flashrank
ENV FLASHRANK_CACHE_DIR=/app/.flashrank_cache
RUN mkdir -p $FLASHRANK_CACHE_DIR

# Force-download the model at build time
RUN python -c "from flashrank import Ranker; Ranker(model_name='ms-marco-MiniLM-L-12-v2', cache_dir='$FLASHRANK_CACHE_DIR')"

# Copy source code
COPY . .

# Copy and set permissions for entrypoint script
COPY scripts/docker/entrypoint.sh /app/scripts/docker/entrypoint.sh
RUN chmod +x /app/scripts/docker/entrypoint.sh

# Prevent uvloop compatibility issues
ENV PYTHONPATH=/app
ENV UVICORN_LOOP=asyncio

# Run
EXPOSE 8000-8001
CMD ["/app/scripts/docker/entrypoint.sh"] 