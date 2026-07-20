from state import MainState, RetriGenState
from utils.logger import logger



def ingestion_router(state: MainState)->str:

    # print(state['ingestion_index'])
    if(state['ingestion_index']<len(state['retrieval_priority'])):
        return 'tool_call'
    else:
        logger.info("Initiating Retrieval and Generation")
        return 'retrieval_initiator'
    

def retrieval_router(state: RetriGenState)->str:

    if()