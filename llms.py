from langchain_groq import ChatGroq
import os
from dotenv import load_dotenv

load_dotenv()

key = os.getenv("GROQ_API_KEY")

llm_llama = ChatGroq(model="llama-3.3-70b-versatile", api_key=key)

llm_oss = ChatGroq(model="openai/gpt-oss-120b")

