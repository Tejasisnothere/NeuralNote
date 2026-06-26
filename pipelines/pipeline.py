from ingestion.YoutubeTranscriptIngestor import YTVideoFetcher
from embedding.embedder import embedding_model
from vector_storage.yt_vector_store import vector_store
from processor.TranscriptProcessor import NormalizeChunks
from uuid import uuid4
 
class YT_search_transcript_storage_pipeline:
    def __init__(self, topic, embedding_model, vector_store, k=5):
        self.topic = topic
        self.embedding_model = embedding_model
        self.vector_store = vector_store
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
            self.vector_store.add_documents(
                documents=docs[i:i+batch_size],
                ids=ids[i:i+batch_size]
            )

        return len(docs)
    


YTF = YT_search_transcript_storage_pipeline(topic="docker", embedding_model=embedding_model, vector_store=vector_store, k=1)

YTF.build()