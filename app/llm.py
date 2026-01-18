import os
from langchain_ollama import ChatOllama

OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")

def get_llm():
    return  ChatOllama(
        model="gemma:2b",
        base_url=OLLAMA_BASE_URL,
        temperature=0.5,
    )

