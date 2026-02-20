FROM python:3.11-slim

RUN apt-get update && \
    apt-get install -y --no-install-recommends libsndfile1 && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY bird_mach/ bird_mach/
COPY scripts/ scripts/

EXPOSE 8000

CMD ["uvicorn", "bird_mach.webapp:app", "--host", "0.0.0.0", "--port", "8000"]
