from langgraph.graph import StateGraph, START, END
import os
from dotenv import load_dotenv
from state import MainState
from nodes import *
from routers import *


load_dotenv()

key = os.getenv("GROQ_API_KEY")


print("key")





graph = StateGraph(MainState)


graph.add_node('refine_query_node', refine_query_node)
graph.add_node('get_user_docs', get_user_docs)
graph.add_node('extract_links', extract_links)
graph.add_node('prioritize_retrieval', prioritize_retrieval)
graph.add_node('ingestion_agent',ingestion_agent)
graph.add_node('retrieval_initiator',retrieval_initiator)
graph.add_node('empty_node',empty_node)

print('nodes')






graph.add_edge(START, 'refine_query_node')


graph.add_edge('refine_query_node','get_user_docs')
graph.add_edge('get_user_docs', 'prioritize_retrieval')
graph.add_edge('prioritize_retrieval', 'extract_links')
graph.add_edge('extract_links','empty_node')
graph.add_conditional_edges(
    "empty_node",
    ingestion_router,
    {
        "tool_call":'ingestion_agent',
        "retrieval_initiator":"retrieval_initiator"
    }

)
graph.add_edge('ingestion_agent', 'empty_node')

graph.add_edge('empty_node', END)






builder = graph.compile()


print('builder')


final_state = builder.invoke({'query':"I want you to generate notes on reinforcement learning. Do not use any pdfs, nor any youtube videos. use this link https://lilianweng.github.io/posts/2018-02-19-rl-overview/",
                              'user_docs':[],
                              'ingestion_index':0,
                              'retrieval_priority':[],
                              'retrieval_priority_score':[]})




print(final_state)




# print(final_state)

print("hello")