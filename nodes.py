from langgraph.graph import START, END, StateGraph
from langchain_classic.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from llms import llm_llama
from pydantic import BaseModel, Field
from state import MainState
from utils.logger import logger
from typing import List

from tools import ingestion_tools
import os
import re


DATA_PATH = os.path.join(os.getcwd(), 'data')


class Topic(BaseModel):
    topic: str = Field(description="Topic about which the user wants to make notes on. Maximum 10 words.")

class SubTopics(BaseModel):
    subtopics: List[str] = Field(description="List of subtopics in order to understand the given topic.")


class PriorityRetreival(BaseModel):
    retrieval_priority: List[str] = Field(description="List of in order pirority of documents for retreival.")
    retrieval_priority_score: List[float] = Field(description="In order score for each document priority.")





def refine_query_node(state: MainState) -> MainState:
    """Refines the user query for effecient understanding by LLM for note making for relevant topic."""

    
    logger.info("Refining user query....")
    
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
    
    query = state['query']

    chain = prompt | llm_llama | StrOutputParser()

    logger.info("Calling llama-3.3-70b-versatile....")
    try:


        response = chain.invoke({'user_query':query})
    
    except Exception as e:
        logger.error("LLm call failed", e)
        return {}
    
    logger.info("LLM call succeeded.")

    topic = extract_topic(query)

    subtopics = generate_subtopics(topic)

    

    




    
    return {'refined_query' : response,
            'topic': topic,
            'subtopics':subtopics}


def extract_links(state: MainState)->MainState:
    user_docs = state['retrieval_priority']

    logger.info("Extracting links")

    print(user_docs)
    print("\n\n\n\n\n")
    links = []
    for i in user_docs:
        initial = i[:4]
        
        if initial == 'http':
            links.append(i)
    


    return {'links':links}


def extract_topic(query: str) -> str:
    logger.info("Extracting topic")

    logger.info("Calling LLM")

    try:

        new_llm = llm_llama.with_structured_output(Topic)
    except Exception as e:
        logger.error("LLM call failed", e)

        return ""
    
    logger.info("LLM call succeeded")

    return new_llm.invoke(query).topic


def generate_subtopics(topic: str):

    logger.info("Generating subtopics")

    try:
        logger.info("Calling LLM....")
        new_llm = llm_llama.with_structured_output(SubTopics)
        subtopics = new_llm.invoke(topic).subtopics

    except Exception as e:
        logger.error("LLM call failed.\n", e)
        return []
    
    return subtopics


def get_user_docs(state: MainState)->MainState:
    from pathlib import Path

    logger.info("Fetching docs provided by the user.")

    USER_DOCS = os.path.join(DATA_PATH, 'user_docs')

    folder = Path(USER_DOCS)

    try:

        files = [file.name for file in folder.iterdir() if file.is_file()]

    except Exception as e:
        logger.error("Failed to fetch docs.\n", e)
        return {'user_docs':[]}

    

    return {'user_docs':files}


def prioritize_retrieval(state: MainState)->MainState:
    new_llm = llm_llama.with_structured_output(PriorityRetreival)

    logger.info("Deciding retrieval priority.")

    prompt = PromptTemplate.from_template(
        """
You are an expert document retrieval planner.

Your task is to determine the order in which documents should be retrieved for generating high-quality notes.

Inputs:
1. Refined user prompt:
{refined_prompt}

2. User-provided documents:
{user_docs}

Instructions:
- Determine all relevant document sources.
- Respect the user's explicitly requested order whenever one is provided.
- If the user does not specify an order, choose the order that is most likely to produce the best notes.
- You may include both user-provided documents and system-retrieved sources.
- System-retrieved sources may include:
  - YouTube Video Transcripts
  - Wikipedia
  - Blogs
- If the user explicitly requests only certain sources, do not include others.
- If both user and system sources are requested, determine the optimal retrieval order.

For every source provide:
1. Source name
2. Source type ("user" or "system")
3. Priority (1 = highest)
4. score between 0.0 and 1.0 based on the requirement of the document.
5. Even if not mentioned score each of the potential retrieval sources.

"""
    )

    chain = prompt | new_llm

    logger.info("Calling LLM. ")

    try:
        response =  chain.invoke({'refined_prompt':state['refined_query'], 'user_docs':state['user_docs']})
    except Exception as e:
        logger.error("LLM call failed.\n", e)
        return {}
    
    return {
        'retrieval_priority':response.retrieval_priority,
        'retrieval_priority_score':response.retrieval_priority_score
    }



def ingestion_router(state: MainState)->str:
    if(state['ingestion_index']<len(state['userdocs'])):
        return 'tool_call'
    else:
        return 'retrieval_planner'


def ingestion_agent(state: MainState)->MainState:
    idx = state['ingestion_index']
    state['ingestion_index'] += 1
    ingested_docs = state['ingested_docs']

    current_doc = ingested_docs[idx]

    

    binded_llm = llm_llama.bind_tools(tools=ingestion_tools)









def retrieval_planner(state:MainState)->MainState:
    return {}