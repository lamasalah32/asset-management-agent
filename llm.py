import os
#from langchain_ollama import ChatOllama
from langchain_openai import ChatOpenAI

#OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")

def get_llm():
    return ChatOpenAI(
        model="gpt-4o-mini",
        temperature=0,
        max_retries=2,
    )




