from ingestion.YoutubeTranscriptIngestor import YTVideoFetcher
from ingestion.BlogIngestor import fetch_and_chunk
from embedding.embedder import embedding_model
from vector_storage.yt_vector_store import transcript_vector_store, blog_vector_store
from processor.TranscriptProcessor import NormalizeChunks
from processor.BlogChunksProcessor import normalize_chunks
import trafilatura
from langchain_text_splitters import RecursiveCharacterTextSplitter
from uuid import uuid4
 
class YT_search_transcript_storage_pipeline:
    def __init__(self, topic, embedding_model, transcript_vector_store, k=5):
        self.topic = topic
        self.embedding_model = embedding_model
        self.transcript_vector_store = transcript_vector_store
        self.k = k

        self.YT_Fetcher = YTVideoFetcher(
            topic=topic,
            embedding_model=embedding_model,
            k=k
        )

    def build(self):
        
        chunks = self.YT_Fetcher.transcriber_chunker()

        docs = NormalizeChunks(chunks)

        ids = [str(uuid4()) for _ in range(len(docs))]

        batch_size = 100

        for i in range(0, len(docs), batch_size):
            self.transcript_vector_store.add_documents(
                documents=docs[i:i+batch_size],
                ids=ids[i:i+batch_size]
            )

        return len(docs)



class BlogStoragePipeline:
    def __init__(self, url):

        self.url = url


    def fetch_store(self):

        chunks = fetch_and_chunk(url=self.url)

        docs = normalize_chunks(chunks=chunks, url=self.url)

        
        
        ids = [str(uuid4()) for _ in range(len(docs))]

        batch_size = 100

        for i in range(0, len(docs), batch_size):
            blog_vector_store.add_documents(
                documents=docs[i:i+batch_size],
                ids=ids[i:i+batch_size]
            )

        return len(docs)






# YTF = YT_search_transcript_storage_pipeline(topic="docker", embedding_model=embedding_model, transcript_vector_store=transcript_vector_store, k=1)

# YTF.build()

bg = BlogStoragePipeline(url="https://transformer-circuits.pub/2025/attention-qk/index.html")

print(bg.fetch_store())