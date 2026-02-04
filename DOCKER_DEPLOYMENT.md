# Docker Deployment Guide

## Quick Start

### 1. Update your `.env` file

Make sure your `.env` file has these variables:

```env
# AstraDB Configuration
ASTRA_DB_API_ENDPOINT=your_astra_db_endpoint
ASTRA_DB_APPLICATION_TOKEN=your_astra_db_token
ASTRA_DB_KEYSPACE=your_keyspace_name

# API Keys
GROQ_API_KEY=your_groq_api_key
HUGGINGFACE_API_TOKEN=your_huggingface_token

# Model Configuration (false for Docker/Groq, true for local Ollama)
USE_OLLAMA=false
```

### 2. Build and Run with Docker Compose

```bash
docker-compose up --build
```

The app will be available at `http://localhost:5000`

### 3. Alternative: Build and Run with Docker

```bash
# Build the image
docker build -t flipkart-recommendation .

# Run the container
docker run -p 5000:5000 \
  -e USE_OLLAMA=false \
  -e ASTRA_DB_API_ENDPOINT=your_endpoint \
  -e ASTRA_DB_APPLICATION_TOKEN=your_token \
  -e ASTRA_DB_KEYSPACE=your_keyspace \
  -e GROQ_API_KEY=your_groq_key \
  -e HUGGINGFACE_API_TOKEN=your_hf_token \
  flipkart-recommendation
```

## Model Configuration

### Using Groq (Recommended for Docker)
- Set `USE_OLLAMA=false` in your `.env` file
- Requires `GROQ_API_KEY`
- No local model server needed
- Works in any cloud environment

### Using Ollama (Local Development)
- Set `USE_OLLAMA=true` in your `.env` file
- Requires Ollama running locally
- Better for development/testing

## Switching Between Models

The system automatically switches between Ollama and Groq based on the `USE_OLLAMA` environment variable:

- **Local Development**: `USE_OLLAMA=true` (uses Ollama)
- **Docker/Cloud**: `USE_OLLAMA=false` (uses Groq)

## Deployment Platforms

### Deploy to Cloud Platforms

The Docker image can be deployed to:
- **AWS ECS/Fargate**
- **Google Cloud Run**
- **Azure Container Instances**
- **DigitalOcean App Platform**
- **Heroku Container Registry**

Just make sure to set the environment variables in your platform's configuration.

## Notes

- The app runs on port 5000 by default
- Make sure your Groq API key has sufficient credits
- AstraDB must be accessible from your deployment environment







