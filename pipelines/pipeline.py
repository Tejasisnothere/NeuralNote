from ingestion.YoutubeTranscriptIngestor import YTVideoFetcher
from embedding.embedder import embedding_model
from vector_storage.yt_vector_store import vector_store

topic = "docker"

class YT_search_transcript_storage_pipeline:
    def __init__(self, topic, embedding_model, k):
        self.YT_Fetcher = YTVideoFetcher(topic=topic, embedding_model=embedding_model, k=k)

        self.metadata = self.YT_Fetcher.metadata

        




YT_Fetcher = YTVideoFetcher(topic=topic, embedding_model=embedding_model, k=5)

metadata = YT_Fetcher.metadata


print(metadata[:4])
# vector_store.add_documents(smart_chunks)


