FROM python:3.12-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt gunicorn

# Copy application code
COPY src/ ./src/
COPY templates/ ./templates/
COPY static/ ./static/
COPY run.py .

# Copy schema and create SQLite database at build time
COPY db/ ./db/
RUN mkdir -p ./db && python -c "import sqlite3; conn = sqlite3.connect('db/uloom_quran.db'); conn.executescript(open('db/schema.sql', encoding='utf-8').read()); conn.close()"

# Copy data files (mutashabihat, exports)
COPY data/mutashabihat/ ./data/mutashabihat/
COPY data/exports/ ./data/exports/

# Expose port (Cloud Run uses 8080)
EXPOSE 8080

# Run with gunicorn (4 workers for concurrency)
CMD ["gunicorn", "src.api.main:app", "-w", "2", "-k", "uvicorn.workers.UvicornWorker", "-b", "0.0.0.0:8080", "--timeout", "120"]
