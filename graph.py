from langgraph.graph import StateGraph, START, END
from langchain_groq import ChatGroq
from langchain.tools import tool
import os
from dotenv import load_dotenv

load_dotenv()

key = os.getenv("GROQ_API_KEY")

