from pipelines.ingestion.WikiIngestor import WikiIngestor
from pipelines.vector_storage.wiki_vector_store import wiki_vector_store
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_classic.schema import Document
from utils.logger import logger
from uuid import uuid4


class WikiPipeline:

    def __init__(self, topic, k=3, max_chars=3000):
        self.ingestor = WikiIngestor(topic=topic, k=k, max_chars=max_chars)
        self.chunk_size = 300
        self.chunk_overlap = 50

        


        

    
    def fetch_chunk_store(self):
        logger.info("Fetching documents from wikipedia")
        raw_docs = self.ingestor.fetch_docs()

        logger.info("splitting wiki documents into chunks")
        splitter =  RecursiveCharacterTextSplitter(raw_docs, chunk_size=self.chunk_size, chunk_overlap=self.chunk_overlap)



        chunks = splitter.split_text(raw_docs)

        docs = [Document(page_content=chunk, metadata={"index":i*self.chunk_size}) for i, chunk in enumerate(chunks)]

        ids = [uuid4() for _ in docs]

        logger.info("Storing documents into vectorstore")
        wiki_vector_store.add_documents(documents=docs, ids=ids)

    



        



