
from langchain_qdrant import QdrantVectorStore
from qdrant_client import QdrantClient
from pipelines.embedding.embedder import embedding_model



client = QdrantClient(host="localhost",port=6333)

pdf_vector_store = QdrantVectorStore(
    client=client,
    collection_name="PDFVectors",
    embedding=embedding_model
)

