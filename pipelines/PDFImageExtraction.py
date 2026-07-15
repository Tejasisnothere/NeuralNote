import fitz  
from pipelines.embedding.embedder import embedding_model
from minio import Minio
import os
from pathlib import Path
import requests
from pipelines.vector_storage.pdf_vector_store import pdf_vector_store
from concurrent.futures import ThreadPoolExecutor
from langchain_classic.schema import Document
from zlib import crc32

class PDFImageExtractor:
    """Image Extraction from a pdf and store to /images/ and image image store"""
    def __init__(self, client_address, bucket_name="neuralnote-images"):

        self.embedding_model = embedding_model
        self.client = Minio(client_address, access_key="admin", secret_key="password123", secure=False)
        self.base_path = os.path.join(os.getcwd(), "data")
        self.pdf_base_path = os.path.join(self.base_path, "pdfs")
        self.image_base_path = os.path.join(self.base_path, "images")
        self.bucket_name = bucket_name
        self.vector_store = pdf_vector_store

        self.executor = ThreadPoolExecutor(max_workers=4)


    def extract_and_store_images(self, pdf_name):
        
        image_path = os.path.join(self.pdf_base_path, pdf_name)


        doc = fitz.open(image_path)

        for page_num in range(len(doc)):
            page = doc[page_num]

            for img_index, img in enumerate(page.get_images(full=True)):
                xref = img[0]

                base_image = doc.extract_image(xref)
                image_bytes = base_image["image"]
                ext = base_image["ext"]

                img_store_base_path = self.image_base_path

                img_name = f"{pdf_name}page{page_num}_img{img_index}new.{ext}"

                image_store_path = os.path.join(img_store_base_path, img_name)

                with open(image_store_path, "wb") as f:
                    f.write(image_bytes)

                self.client.fput_object(
                    bucket_name=self.bucket_name,
                    object_name=img_name,
                    file_path=image_store_path
                )

                self.executor.submit(self.image_ocr, img_name, page_num, pdf_name)


        



                

    
    def image_ocr(self, image_name, page_num, file_name):
        
        
        
        try:
            
            response = requests.post(
                "http://localhost:8000/ocr",
                json={
                    "filename":image_name
                }
            )

            ocr = response.text

            if ocr:

                doc = [Document(page_content=ocr, metadata={"type":"image", "page":page_num, "file_name":file_name, "image_name":image_name})]
                ids = [crc32(image_name.encode())]
                self.vector_store.add_documents(documents=doc, ids=ids)


            image_path = os.path.join(self.image_base_path,image_name)

            os.remove(image_path)

            # os.remove(image_name) // m so stupid :sob:
        except Exception as e:
            print(e)




# instance = PDFImageExtractor("localhost:9000")
# instance.extract_and_store_images('blackholes.pdf')