
from langchain_qdrant import QdrantVectorStore
from qdrant_client import QdrantClient
from embedding.embedder import embedding_model



client = QdrantClient(host="localhost",port=6333)

blog_vector_store = QdrantVectorStore(
    client=client,
    collection_name="BlogVectors",
    embedding=embedding_model
)

