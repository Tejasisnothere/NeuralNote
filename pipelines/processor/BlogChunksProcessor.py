from langchain_classic.schema import Document


def normalize_chunks(chunks, url):
    docs = [Document(page_content=chunk, metadata={'url':url}) for chunk in chunks]

    return docs