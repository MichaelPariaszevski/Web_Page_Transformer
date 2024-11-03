from langchain_openai import ChatOpenAI 
from langchain_groq import ChatGroq 
from langchain_ollama import ChatOllama

def llm_selection(model: str): 
        gpt_model_list = ["gpt-4o", "gpt-4o-mini"]
        llama_model_list = ["llama-3.1-70b-versatile", "llama-3.1-8b-instant", "llama-3.2-1b-preview", "llama-3.2-3b-preview"]
        ollama_model_list = ["deepseek-coder-v2:16b", "llama3.1:8b", "llama3.1:70b", "llama3.2:3b"]
        if "gpt" in model.lower() and model.lower() in gpt_model_list: 
            return ChatOpenAI(model = model.lower(), temperature = 0)
        elif "llama" in model.lower() and model.lower() in llama_model_list: 
            return ChatGroq(model = model.lower(), temperature = 0)
        elif "deepseek" or "llama" in model.lower() and model.lower() in ollama_model_list: 
            return ChatOllama(model = model.lower(), temperature = 0)
        else: 
            raise Exception("Invalid LLM model provided\n\nValid Models:\nOpenAI: ['gpt-4o', 'gpt-4o-mini']\nChatGroq: ['llama-3.1-70b-versatile', 'llama-3.1-8b-instant', 'llama-3.2-1b-preview', 'llama-3.2-3b-preview']")