# 🛒 Flipkart Product Recommender System

An intelligent product recommendation system for Flipkart, powered by RAG (Retrieval-Augmented Generation), LangChain, and AstraDB. This system analyzes product reviews to provide context-aware recommendations through a conversational interface.

## 🌟 Features

- **AI-Powered Recommendations**: Uses GROQ LLM (Llama 3) for intelligent, review-based suggestions.
- **RAG Architecture**: Leverages Retrieval-Augmented Generation for accurate information retrieval from Flipkart product data.
- **Vector Search**: High-performance similarity search using AstraDB (Cassandra) and HuggingFace embeddings.
- **Conversational Interface**: Clean Flask-based web UI for natural language interaction.
- **Full Observability**: Integrated monitoring stack with Prometheus and Grafana for tracking system metrics.
- **Cloud-Ready**: Ready for deployment via Docker, Docker Compose, and Kubernetes.

## 🛠️ Tech Stack

- **LLM**: GROQ API (Llama 3.3)
- **Vector Database**: AstraDB (DataStax Cassandra)
- **Embeddings**: HuggingFace (Sentence Transformers)
- **Framework**: LangChain (LCEL)
- **Backend**: Flask
- **Monitoring**: Prometheus & Grafana
- **Containerization**: Docker
- **Orchestration**: Kubernetes (K8s)
- **Language**: Python 3.11

## 📁 Project Structure

```
Flipkart Product recommendation/
├── app.py                      # Flask application entry point
├── flipkart/                   # Core application modules
│   ├── data_ingestion.py      # Data loading and vector ingestion
│   ├── rag_chain.py           # LangChain RAG pipeline
│   ├── data_converter.py      # Data transformation logic
│   └── config.py              # Configuration & Environment setup
├── data/                       # Dataset directory
│   └── flipkart_product_review.csv
├── prometheus/                 # Prometheus configuration & K8s manifests
├── grafana/                    # Grafana deployment manifests
├── templates/                  # HTML templates
├── static/                     # CSS & Static assets
├── utils/                      # Logging & Exception handling
├── Dockerfile                  # Container configuration
├── docker-compose.yml          # Multi-container orchestration
├── flask-deployment.yaml       # Kubernetes deployment for Flask
└── requirements.txt            # Python dependencies
```

## 🚀 Getting Started

### Prerequisites

- Python 3.11 or higher
- [GROQ API Key](https://console.groq.com)
- [AstraDB Account](https://astra.datastax.com) (Endpoint, Token, and Keyspace)
- [HuggingFace Token](https://huggingface.co/settings/tokens)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/deep1305/FLIPKART-PRODUCT-RECOMMENDER-SYSTEM.git
   cd "Flipkart Product recommendation"
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**
   
   Create a `.env` file in the root directory:
   ```env
   ASTRA_DB_API_ENDPOINT=your_astradb_endpoint
   ASTRA_DB_APPLICATION_TOKEN=your_astradb_token
   ASTRA_DB_KEYSPACE=your_keyspace_name
   GROQ_API_KEY=your_groq_api_key
   HUGGINGFACE_API_TOKEN=your_huggingface_token
   USE_OLLAMA=false
   FLASK_DEBUG=false
   ```

4. **Run the application**
   ```bash
   python app.py
   ```

5. **Open your browser** to `http://localhost:5000`

## 🐳 Docker Deployment

Build and run the entire stack using Docker Compose:

```bash
# Build and start all services (Flask, Prometheus, Grafana)
docker-compose up --build
```

Access:
- Flask App: `http://localhost:5000`
- Prometheus: `http://localhost:9090`

## ☸️ Kubernetes Deployment

Deploy to a Kubernetes cluster (GKE, Minikube, etc.):

```bash
# 1. Create secrets
kubectl create secret generic llmops-secrets \
  --from-literal=ASTRA_DB_API_ENDPOINT=... \
  --from-literal=ASTRA_DB_APPLICATION_TOKEN=... \
  --from-literal=ASTRA_DB_KEYSPACE=... \
  --from-literal=GROQ_API_KEY=... \
  --from-literal=HUGGINGFACE_API_TOKEN=...

# 2. Apply manifests
kubectl apply -f flask-deployment.yaml
kubectl apply -f prometheus/
kubectl apply -f grafana/

# 3. Check status
kubectl get pods -n monitoring
kubectl get pods (default namespace)
```

## 📊 How It Works

1. **Data Ingestion**: Flipkart product reviews are processed and converted into vector embeddings using HuggingFace models.
2. **Vector Storage**: These embeddings are stored in AstraDB for efficient semantic retrieval.
3. **Retrieval**: When a user asks a question, the system retrieves relevant product reviews from the vector store.
4. **Augmented Generation**: The retrieved context is passed to the GROQ LLM (Llama 3) to generate a personalized recommendation.
5. **Observability**: Every request increments metrics scraped by Prometheus and visualized in Grafana.

## 🙏 Acknowledgments

- Flipkart dataset for product review data.
- [LangChain](https://langchain.com) for the RAG orchestration.
- [DataStax AstraDB](https://astra.datastax.com) for serverless Cassandra.
- [GROQ](https://groq.com) for lightning-fast LLM inference.

---

**Made with ❤️ for the E-commerce Community**
