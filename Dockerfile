FROM python:3.11-slim

LABEL org.opencontainers.image.title="Mach"
LABEL org.opencontainers.image.description="Audio visualization web app"

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

RUN apt-get update && \
    apt-get install -y --no-install-recommends libsndfile1 && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY bird_mach/ bird_mach/
COPY scripts/ scripts/

EXPOSE 8000

CMD ["sh", "-c", "uvicorn bird_mach.webapp:app --host 0.0.0.0 --port ${PORT:-8000}"]
