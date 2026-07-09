from langgraph.graph import StateGraph, START, END
from langchain_groq import ChatGroq
from langchain.tools import tool
import os
from dotenv import load_dotenv
from state import MainState
from nodes import *


load_dotenv()

key = os.getenv("GROQ_API_KEY")




graph = StateGraph(MainState)


graph.add_node('refine_query_node', refine_query_node)
graph.add_node('get_user_docs', get_user_docs)
graph.add_node('prioritize_retrieval', prioritize_retrieval)







graph.add_edge(START, 'refine_query_node')


graph.add_edge('refine_query_node','get_user_docs')
graph.add_edge('get_user_docs', 'prioritize_retrieval')
graph.add_edge('prioritize_retrieval', END)



builder = graph.compile()


final_state = builder.invoke({'query':"Generate comprehensive notes on Reinforcement Learning. Use my uploaded RL Lecture Notes.pdf first, then supplement with Wikipedia and YouTube transcripts wherever necessary. also i have this https://blog.ml.cmu.edu/category/reinforcement-learning/",
                              'user_docs':[]})


print(final_state)
