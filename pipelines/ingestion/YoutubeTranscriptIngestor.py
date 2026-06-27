import yt_dlp
from sklearn.metrics.pairwise import cosine_similarity
from langchain_text_splitters import RecursiveCharacterTextSplitter
from youtube_transcript_api import YouTubeTranscriptApi
import requests
import os 
from dotenv import load_dotenv

load_dotenv()


API_KEY = os.getenv("TRANSCRIPT_API_KEY")


class YTVideoFetcher:
    def __init__(self, topic, embedding_model, k=20):
        self.embedding_model = embedding_model
        
        self.topic = topic
        
        self.k = k
        self.imp_params = ['title', 'id', 'description', 'duration', 'view_count', 'like_count', 'webpage_url', 'language']
        self.url = f"ytsearch{k}:{self.topic}"
        self.ydl = yt_dlp.YoutubeDL({
            "queit":True
        })
        self.results = []
        self.lang_check()


        self.search_videos()
        self.metadata = self.extract_metadata()

        

    def lang_check(self):
        self.results["entries"] = [video for video in self.results["entries"] if video.get("language") == "en"]

        

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
    

    
    
    
    

    def get_transcripts(self)->dict:
        data = {}
        for video in self.metadata:

            video_id = video['id']
            
            url = 'https://transcriptapi.com/api/v2/youtube/transcript'
            params = {'video_url': video_id, 'format': 'json'}
            r = requests.get(url, params=params, headers={'Authorization': f'Bearer {API_KEY}'}, timeout=30)
            r.raise_for_status()
            transcript = r.json()['transcript']
            
            data[video_id] = transcript
        
        return data
        
        

    def chunk_transcript(self, data, max_chars=500):
        chunks = []

        for video_id, transcript in data.items():

            current_text = []
            start_time = None
            current_len = 0

            for seg in transcript:

                text = seg["text"]

                if start_time is None:
                    start_time = seg["start"]

                if current_len + len(text) > max_chars and current_text:

                    chunks.append({
                        "text": " ".join(current_text),
                        "start_time": start_time,
                        "end_time": seg["start"],
                        "video_id": video_id
                    })

                    current_text = []
                    start_time = seg["start"]
                    current_len = 0

                current_text.append(text)
                current_len += len(text)

            # Store the final chunk of this video
            if current_text:
                last_seg = transcript[-1]

                chunks.append({
                    "text": " ".join(current_text),
                    "start_time": start_time,
                    "end_time": last_seg["start"] + last_seg["duration"],
                    "video_id": video_id
                })

        return chunks
    
    def transcriber_chunker(self):
        data = self.get_transcripts()
        return self.chunk_transcript(data)
