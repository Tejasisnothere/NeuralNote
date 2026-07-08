from langgraph.graph import START, END, StateGraph
from langchain_classic.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from llms import llm_llama
from pydantic import BaseModel, Field


class Topic(BaseModel):
    topic: str = Field(description="Topic about which the user wants to make notes on. Maximum 10 words.")


def refine_query(query: str) -> str:
    """Refines the user query for effecient understanding by LLM for note making for relevant topic."""
    
    prompt = PromptTemplate.from_template(
            """
You are an expert query refinement assistant.

Your task is to rewrite the user's query so that its intent is clear, specific, and unambiguous for a note-generation system.

The system can generate notes from the following sources:
- YouTube transcripts
- PDFs
- Blogs or web articles
- User-uploaded documents

Instructions:
1. Identify the user's primary intent.
2. Preserve all information provided by the user.
3. Clearly mention the preferred source if the user specifies one.
4. If the source is not specified, do not assume one. Simply state that no preferred source was mentioned.
5. Do not add new information or change the meaning of the request.
6. Return only the refined query.
7. The refined query must be no more than 150 words.
8. Only tell what user wants dont add unecessary text.

User Query:
{user_query} """
        )
    
    chain = prompt | llm_llama | StrOutputParser()

    response = chain.invoke({'user_query':query})


    return response


def extract_topic(query: str) -> str:
    new_llm = llm_llama.with_structured_output(Topic)
    return new_llm.invoke(query).topic


query = "Make notes on docker volumes i have attached some files prefer these more and fetch something oneline too\nFiles:\ndocker tutorial 1\ndocker guide"
resp = refine_query(query)
print(resp)
print(extract_topic(resp))