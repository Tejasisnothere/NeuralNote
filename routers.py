from state import MainState




def ingestion_router(state: MainState)->str:
    if(state['ingestion_index']<len(state['user_docs'])):
        return 'tool_call'
    else:
        return 'retrieval_initiator'