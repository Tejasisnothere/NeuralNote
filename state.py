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
    query: str = Field(description="Intial User query for notes generation on certain topic")
    refined_query: str = Field(description="Refined description of user query more detailed")

    user_docs: List[str] = Field(description="Name of documents uploaded by the user for reference")


    retrieval_priority: List[str] = Field(description="Increasing order of priority for refering stores for retrieval.")
    retrieval_priority_score: List[int]


    subtopics: List[str] = Field(description="List of subtopics planned for note generation")
    
    



    