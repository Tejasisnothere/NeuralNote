import trafilatura
from langchain_text_splitters import RecursiveCharacterTextSplitter


        


def fetch_blog( url):
    downloaded = trafilatura.fetch_url(url)
    text = trafilatura.extract(downloaded)

    return text

def chunker(text):
    splitter = RecursiveCharacterTextSplitter(chunk_size=300, chunk_overlap=50)

    chunks = splitter.split_text(text)

    return chunks


def fetch_and_chunk(url):

    text = fetch_blog(url)

    chunks = chunker(text=text)

    return chunks




