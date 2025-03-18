import pymongo
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import MongoDBAtlasVectorSearch
from typing import List, Dict
import json

class MongoDBUploader:
    def __init__(self, mongodb_uri: str, db_name: str, collection_name: str, llm_api_key: str):
        self.client = pymongo.MongoClient(mongodb_uri)
        self.db = self.client[db_name]
        self.collection = self.db[collection_name]
        self.embedding_model = OpenAIEmbeddings(api_key=llm_api_key)
        self.vector_store = MongoDBAtlasVectorSearch(
            collection=self.collection, embedding=self.embedding_model
        )

    def upload_multimodal_data(self, documents: List[Dict[str, str]]):
        """
        Uploads multimodal data (text and potentially image embeddings) to MongoDB Vector Search.
        Each document should have 'text' and optionally 'image_path' or 'image_embedding'.
        """
        texts = []
        embeddings = []
        metadata = []

        for doc in documents:
            text = doc.get("text", "")
            texts.append(text)
            embedding = self.embedding_model.embed_query(text)
            embeddings.append(embedding)
            
            # Handle potential image data (simplified example)
            image_path = doc.get("image_path", None)
            image_embedding = doc.get("image_embedding", None)  # Precomputed or computed here
            meta = {"text": text, "source": "user_upload"}
            if image_path:
                meta["image_path"] = image_path
            if image_embedding:
                meta["image_embedding"] = image_embedding
            metadata.append(meta)

        # Upload to MongoDB Vector Search
        self.vector_store.add_texts(texts, embeddings=embeddings, metadatas=metadata)
        print(f"Uploaded {len(texts)} documents to MongoDB Vector Search.")

    def verify_upload(self, query: str):
        """Verify upload by searching for a sample query."""
        results = self.vector_store.similarity_search(query, k=3)
        print(f"Verification search results for '{query}':")
        for res in results:
            print(f"- {res.page_content[:100]}... (metadata: {res.metadata})")

# Example usage
if __name__ == "__main__":
    LLM_API_KEY = "your-openai-api-key"
    MONGODB_URI = "mongodb+srv://user:pass@cluster0.mongodb.net/"
    
    uploader = MongoDBUploader(MONGODB_URI, "quantum_db", "vectors", LLM_API_KEY)
    
    # Sample multimodal documents
    sample_docs = [
        {"text": "Quantum teleportation uses entanglement to transfer states.", "image_path": "teleportation_diagram.png"},
        {"text": "Grover's algorithm provides quadratic speedup for search.", "image_embedding": [0.1, 0.2, 0.3]}  # Example embedding
    ]
    
    uploader.upload_multimodal_data(sample_docs)
    uploader.verify_upload("quantum teleportation")