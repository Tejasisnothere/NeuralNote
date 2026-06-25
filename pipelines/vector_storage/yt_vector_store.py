from pinecone import Pinecone
from langchain_pinecone import PineconeVectorStore
import os
from embedding.embedder import embedding_model
from dotenv import load_dotenv
load_dotenv()


from pinecone import Pinecone
import os
key = os.getenv("PINECONE_API_KEY")
pc = Pinecone(api_key = key)

index = pc.Index('neural-note')


vector_store = PineconeVectorStore(index=index, embedding=embedding_model)





