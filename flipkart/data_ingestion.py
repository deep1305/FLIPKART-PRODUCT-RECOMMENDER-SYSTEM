import os
from langchain_astradb import AstraDBVectorStore
from langchain_huggingface import HuggingFaceEndpointEmbeddings
from flipkart.config import Config
from flipkart.data_converter import DataConverter

class DataIngestion:
    def __init__(self):
        self.config = Config()
        self.embedding = HuggingFaceEndpointEmbeddings(model = self.config.EMBEDDING_MODEL, huggingfacehub_api_token = self.config.HUGGINGFACE_API_TOKEN)
        
        self.vector_store = AstraDBVectorStore(
            embedding = self.embedding,
            collection_name = "flipkart",
            api_endpoint = self.config.ASTRA_DB_API_ENDPOINT,
            token = self.config.ASTRA_DB_APPLICATION_TOKEN,
            namespace = self.config.ASTRA_DB_KEYSPACE
        )

    def ingest(self, load_existing = True):
        if load_existing==True:
            return self.vector_store

        # Get the project root directory (parent of flipkart directory)
        current_dir = os.path.dirname(os.path.abspath(__file__))
        project_root = os.path.dirname(current_dir)
        csv_path = os.path.join(project_root, "data", "flipkart_product_review.csv")
        
        docs = DataConverter(file_path = csv_path).convert()

        self.vector_store.add_documents(docs)

        return self.vector_store

'''
if __name__ == "__main__":
    ingestor = DataIngestion()
    ingestor.ingest(load_existing = False)
    '''