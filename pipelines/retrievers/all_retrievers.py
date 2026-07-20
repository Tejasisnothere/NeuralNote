from vector_storage.yt_vector_store import transcript_vector_store
from vector_storage.pdf_vector_store import pdf_vector_store
from vector_storage.wiki_vector_store import wiki_vector_store
from vector_storage.blog_vector_store import blog_vector_store


yt_retriever = transcript_vector_store.as_retriever(search_type='mmr',search_kwargs={"k":4})
pdf_retriever = pdf_vector_store.as_retriever(search_type='mmr',search_kwargs={"k":4})
blog_retriever = blog_vector_store.as_retriever(search_type='mmr',search_kwargs={"k":4})
wiki_retriever = wiki_vector_store.as_retriever(search_type='mmr',search_kwargs={"k":4})

