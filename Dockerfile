FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY . .

# Create necessary directories
RUN mkdir -p logs cache data/excel data/reports

# Run server
CMD ["uvicorn", "src.palmer_ai.server:app", "--host", "0.0.0.0", "--port", "8000"]
