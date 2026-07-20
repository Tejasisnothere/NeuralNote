from langchain.tools import tool
from pipelines.BlogPipeline import BlogStoragePipeline
from pipelines.YT_Pipeline import YT_search_transcript_storage_pipeline
from pipelines.embedding.embedder import embedding_model
from pipelines.PDFIngestionPipeline import PDFIngestor
from utils.logger import logger

from pipelines.PDFImageExtraction import PDFImageExtractor

from pipelines.vector_storage.yt_vector_store import transcript_vector_store

from pipelines.WikipediaPipeline import WikiPipeline






@tool
def intiate_blog_storage_pipeline(link: str):
    """Initiates the blog storage pipeline and stores documents with respect to the provided link into the vectorstore"""

    logger.info("Executing blog storage pipeline")

    BlogSP = BlogStoragePipeline(link)

    BlogSP.fetch_store()




@tool
def initiate_YT_transcript_pipeline(topic: str):
    """Intitiates the youtube video search and transcript storage pipeline into the corresponding vector store"""

    logger.info("Executing youtube transcript extraction and storage pipeline")

    YTT_pipeline = YT_search_transcript_storage_pipeline(topic=topic, embedding_model=embedding_model, transcript_vector_store=transcript_vector_store)


    YTT_pipeline.build()






@tool
def PDF_extraction_storage_pipeline(filename: str):
    """Initiate the pdf text and images storage pipeline to store documents from pdf into corresponding vector store"""
## GOtta have that file inside data/pdfs tho


    logger.info("Executing pdf storage pipeline")
    pdi = PDFIngestor()
    pdi.ingestPDF(filename)


    pdf_images_extractor = PDFImageExtractor(client_address="localhost:9000")

    pdf_images_extractor.extract_and_store_images(filename)


@tool
def Wikipedia_extraction_storage_pipeline(topic: str):

    """Initiate the wikipedia pipeline to extract documents rom wikipedia for user query."""

    wk = WikiPipeline(topic=topic, k=3, max_chars=5000)

    wk.fetch_chunk_store()






ingestion_tools = [intiate_blog_storage_pipeline, intiate_blog_storage_pipeline, PDF_extraction_storage_pipeline, Wikipedia_extraction_storage_pipeline]


