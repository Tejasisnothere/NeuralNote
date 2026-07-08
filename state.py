from langgraph.graph import StateGraph
from langgraph.graph.message import add_messages
from pydantic import BaseModel, Field
from typing import TypedDict, Annotated, List
from langchain_classic.schema import Document




class RetrievalPriority(BaseModel):
    priority_order: List = Field(description="Descending order of priority of vector stores for retrieval")

class GenerateTopics(BaseModel):
    topics: List = Field(description="Ordered list of topics for note-making for the user query.")



class MainState(TypedDict):
    planned_topics: List[str] = Field(description="")
    
    user_query: str = Field(description="Query entered by user.")


    