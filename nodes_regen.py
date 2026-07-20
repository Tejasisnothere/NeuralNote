from langgraph.graph import START, END, StateGraph
from langchain_classic.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from llms import llm_llama
from pydantic import BaseModel, Field
from state import MainState, RetriGenState
from utils.logger import logger
from typing import List, Literal



class Section(BaseModel):
    id: int = Field(description="Unique section number")
    title: str = Field(description="section title")
    importance: Literal["high", "medium", "low"]
    estimated_depth: Literal["brief", "medium", "detailed"]

class SectionPlan(BaseModel):
    sections: List[Section]



def retrieval_initiator(state:MainState)->MainState:
    

    return {}


def subtopics_generator(state2: MainState, state:RetriGenState)->RetriGenState:
    user_query = state2['refined_query']
    main_topic = state2['topic']
    topic = state['topic']
    structured_llm = llm_llama.with_structured_output(SectionPlan)

    

    prompt = PromptTemplate.from_template("""
    You are an expert technical content planner.

    Main Topic:
    {main_topic}

    Current Subtopic:
    {subtopic}

    User Query:
    {user_query}

    Your task is to decompose ONLY the current subtopic into a logical sequence of finer-grained sections that together form a complete explanation.

    Rules:
    - Generate between 5 and 12 sections.
    - Order them from introductory to advanced.
    - Avoid overlapping sections.
    - Focus only on the current subtopic.
    - Include mathematical concepts, algorithms, examples, and practical considerations when applicable.
    - Do not introduce unrelated concepts.

    Return ONLY valid JSON.

    {{
        "sections": [
            {{
                "id": 1,
                "title": "..."
            }}
        ]
    }}
    """)

    response = structured_llm.invoke(prompt.format(main_topic=main_topic, subtopic=topic, user_query=user_query))

    return {'section_plan':response.sections}
    


    
