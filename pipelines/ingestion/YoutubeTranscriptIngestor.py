import yt_dlp
from langchain_huggingface import HuggingFaceEmbeddings
from sklearn.metrics.pairwise import cosine_similarity
from langchain_text_splitters import RecursiveCharacterTextSplitter
import YoutubeTranscriptIngestor



class YTVideoFetcher:
    def __init__(self, topic, embedding_model, k=5):
        self.embedding_model = embedding_model
        
        self.topic = topic
        
        self.k = k
        self.imp_params = ['title', 'id', 'description', 'duration', 'view_count', 'like_count', 'webpage_url']
        self.url = f"ytsearch{k}:{self.topic}"
        self.ydl = yt_dlp.YoutubeDL({
            "queit":True
        })
        self.results = []
        self.search_videos()
        self.metadata = self.extract_metadata()

        self.ytt = YoutubeTranscriptIngestor()

        self.transcript_data = {}

        

    def search_videos(self):

        self.results = self.ydl.extract_info(
            self.url,
            download=False
        )
    
    def extract_metadata(self):

        metadata = []

        for video in self.results["entries"]:

            video_data = {}

            for param in self.imp_params:
                video_data[param] = video.get(param)

            metadata.append(video_data)

        return metadata
    
    def filter_docs(self):
        topic_embedding = self.embedding_model.embed_query(
            self.topic
        )

        texts = [
            f"{doc['title']} {doc['description'][:500]}"
            for doc in self.metadata
        ]

        doc_embeddings = self.embedding_model.embed_documents(
            texts
        )

        for doc, emb in zip(self.metadata, doc_embeddings):
            doc["semantic_score"] = cosine_similarity(
                [topic_embedding],
                [emb]
            )[0][0]

        self.metadata.sort(
            key=lambda x: x["semantic_score"],
            reverse=True
        )

        self.metadata = self.metadata[: max(1, self.k // 2)]

        self.metadata.sort(
            key=lambda x: (
                x.get("view_count", 0),
                x.get("like_count", 0) or 0
            ),
            reverse=True
        )

        return self.metadata
    
    def get_transcripts(self):
        for video in self.metadata:
            id = video['id']
            transcript = self.ytt.fetch(id)
            self.transcript_data[video] = transcript

    def chunk_transcript(self,transcript,max_chars=500):
        chunks = []

        current_text = []
        start_time = None
        current_len = 0

        for seg in transcript:
            text = seg.text

            if start_time is None:
                start_time = seg.start

            if current_len + len(text) > max_chars:

                end_time = seg.start

                chunks.append({
                    "content": " ".join(current_text),
                    "start_time": start_time,
                    "end_time": end_time
                })

                current_text = []
                start_time = seg.start
                
                current_len = 0

            current_text.append(text)
            current_len += len(text)

        return chunks

        
