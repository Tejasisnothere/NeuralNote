from langchain_classic.schema import Document


def NormalizeChunks(chunks):
    
    docs = [Document(page_content=chunk['text'], metadata={'start_time':chunk['start_time'], 'end_time':chunk['end_time'], 'video_id':chunk['video_id']}) for chunk in chunks]

    return docs