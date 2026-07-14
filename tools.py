from langchain.tools import tool
from pipelines.BlogPipeline import BlogStoragePipeline
from pipelines.YT_Pipeline import YT_search_transcript_storage_pipeline
from pipelines.embedding.embedder import embedding_model

from pipelines.vector_storage.yt_vector_store import transcript_vector_store




@tool
def intiate_blog_storage_pipeline(link: str):
    """Initiates the blog storage pipeline and stores documents with respect to the provided link into the vectorstore"""

    BlogSP = BlogStoragePipeline(link)

    BlogSP.fetch_store()




@tool
def initiate_YT_transcript_pipeline(topic: str):
    """Intitiates the youtube video search and transcript storage pipeline into the corresponding vector store"""


    YTT_pipeline = YT_search_transcript_storage_pipeline(topic=topic, embedding_model=embedding_model, transcript_vector_store=transcript_vector_store)


    YTT_pipeline.build()





