from langchain_community.document_loaders import PyMuPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_classic.schema import Document
from vector_storage.pdf_vector_store import pdf_vector_store
import os
import zlib
PDF_PATH = os.path.join(os.getcwd(), 'data', 'pdfs')



class PDFIngestor:
    def __init__(self):
        self.splitter = RecursiveCharacterTextSplitter(chunk_size=300, chunk_overlap=50)


    def get_id_filename(self, file_name):
        return zlib.crc32(file_name)
    
    def ingestPDF(self, file_name):
        file_path = os.path.join(PDF_PATH, file_name)
        loader = PyMuPDFLoader(file_path=file_path, mode="page")

        file_unique_id = self.get_id_filename(file_name.encode())
        
        
        for idx, page in enumerate(loader.lazy_load()):
            text = page.page_content

            chunks = self.splitter.split_text(text=text)
            docs = [Document(page_content=chunk, metadata={"page_no":page.metadata['page'], "file_name":file_name}) for chunk in chunks]
            ids = [int(str(file_unique_id)+str(00)+str(idx)+str(00)+str(i)) for i in range(len(chunks))]

            pdf_vector_store.add_documents(documents=docs, ids=ids)



# pdi = PDFIngestor()

# pdi.ingestPDF("Tejas_Kadam_Resume.pdf")


            
        


# print(PDF_PATH)