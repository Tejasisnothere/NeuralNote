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
    links: List[str] = Field(description="Links provided by the user could potentially be (blogs, wikipedia, etc)")


    retrieval_priority: List[str] = Field(description="Increasing order of priority for refering stores for retrieval.")
    retrieval_priority_score: List[int]


    ingested_docs: List[str] = Field(description="List of all ingested documents")

    ingestion_index: int

    tool_calls: List = Field(description="List of all tool calls made")

    subtopics: List[str] = Field(description="List of subtopics planned for note generation")




## Eventually wed make automatic query retriever basic thought process -> subtopic -> planner (plans subtopics of subtopics) -> smart retreiver(generates queries for retrieving theese subtopics) -> retreives

    
    
    



    