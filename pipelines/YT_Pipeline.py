from ingestion.YoutubeTranscriptIngestor import YTVideoFetcher
from ingestion.BlogIngestor import fetch_and_chunk
from embedding.embedder import embedding_model
from vector_storage.yt_vector_store import transcript_vector_store, blog_vector_store
from processor.TranscriptProcessor import NormalizeChunks
from processor.BlogChunksProcessor import normalize_chunks


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

