from ingestion.YoutubeTranscriptIngestor import YTVideoFetcher
from ingestion.BlogIngestor import fetch_and_chunk
from embedding.embedder import embedding_model
from vector_storage.yt_vector_store import transcript_vector_store, blog_vector_store
from processor.TranscriptProcessor import NormalizeChunks
from processor.BlogChunksProcessor import normalize_chunks
from uuid import uuid4

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





