from pinecone import Pinecone
from langchain_pinecone import PineconeVectorStore
import os
from embedding.embedder import embedding_model
from dotenv import load_dotenv
load_dotenv()



### INITIALLY I WS USING PINECONE HOWEVER  I  THOUGHT I MIGHT RUN OUT OF CREDITS WHICH I WONT IK BUT I WANTED TO TEST Qdrant


# from pinecone import Pinecone
# import os
# key = os.getenv("PINECONE_API_KEY")
# pc = Pinecone(api_key = key)

# index = pc.Index('neural-note')


# vector_store = PineconeVectorStore(index=index, embedding=embedding_model)


from langchain_qdrant import QdrantVectorStore
from qdrant_client import QdrantClient



# client = QdrantClient(":memory:")  -->>> for in memory storage of vectors


client = QdrantClient(host="localhost",port=6333)

transcript_vector_store = QdrantVectorStore(
    client=client,
    collection_name="YoutubeTranscripts",
    embedding=embedding_model
)







