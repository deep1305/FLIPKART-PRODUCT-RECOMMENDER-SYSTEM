# Use Python 3.11 slim image
FROM python:3.11-slim

# Essential environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    USE_OLLAMA=false \
    FLASK_DEBUG=false

# Set working directory
WORKDIR /app

# Install system dependencies only if needed by Python packages
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire project
COPY . .

# Expose port 5000
EXPOSE 5000

# run the application
CMD ["python", "app.py"]


