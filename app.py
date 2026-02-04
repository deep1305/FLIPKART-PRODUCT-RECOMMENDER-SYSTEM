import os
from flask import render_template, request, Flask, Response
from prometheus_client import Counter, generate_latest

from flipkart.data_ingestion import DataIngestion
from flipkart.rag_chain import RAGChainBuilder

from dotenv import load_dotenv

load_dotenv()

REQUEST_COUNT = Counter("http_requests_total", "Total HTTP Requests")


def create_app():
    app = Flask(__name__)
    vector_store = DataIngestion().ingest(load_existing = True)
    rag_chain = RAGChainBuilder(vector_store).build_chain()

    @app.route("/")
    def index():
        REQUEST_COUNT.inc()
        return render_template("index.html")

    @app.route("/get", methods=["POST"])
    def get_response():
        REQUEST_COUNT.inc()
        try:
            user_input = request.form["msg"]
            # With the new LCEL chain, the output is the string directly
            response = rag_chain.invoke({"input": user_input}, config={"configurable": {"session_id": "user-session"}})
            return response
        except Exception as e:
            return f"Error: {str(e)}", 500
    
    @app.route("/metrics")
    def metrics():
        return Response(generate_latest(), mimetype="text/plain")
    
    return app

if __name__ == "__main__":
    app = create_app()
    # Debug mode: True for development, False for production
    debug_mode = os.getenv("FLASK_DEBUG", "True").lower() == "true"
    app.run(host="0.0.0.0", port=5000, debug=debug_mode)