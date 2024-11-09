from google.generativeai import TextGenerationModel  # For Gemini token counting
from langchain_openai import ChatOpenAI
from langchain.chains import LLMChain
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import ChatPromptTemplate
from langchain_text_splitters import Language, RecursiveCharacterTextSplitter
from langchain_groq import ChatGroq
from bs4 import BeautifulSoup
from Web_Page_Class_and_Tests_2.Web_Page_Prompt_Templates.Chunks import template_chunks
import asyncio
import time 
import math
import tiktoken
from dotenv import load_dotenv, find_dotenv 

load_dotenv(find_dotenv(), override = True) 

def count_tokens(text: str, model: str = "gemini-1.5-flash-002") -> int:
    """Count tokens for text using model-specific tokenizers"""
    
    # Gemini-specific token counting
    if "gemini" in model.lower():
        try:
            # Initialize Gemini tokenizer
            gemini_model = TextGenerationModel(model_name=model)
            return gemini_model.count_tokens(text)
        except Exception as e:
            print(f"Error with Gemini tokenizer: {e}")
            # Fallback to approximate count for Gemini (chars/4)
            return len(text) // 4
    
    # OpenAI/GPT models
    elif "gpt" in model.lower():
        try:
            encoder = tiktoken.encoding_for_model(model)
            return len(encoder.encode(text))
        except KeyError:
            encoder = tiktoken.get_encoding("cl100k_base")
            return len(encoder.encode(text))
    
    # Default fallback
    else:
        encoder = tiktoken.get_encoding("cl100k_base")
        return len(encoder.encode(text))

def split_html_by_tokens(html_content: str, max_tokens: int = 800000, model: str = "gemini-1.5-flash-002") -> list:
    """Split HTML content into chunks that don't exceed max_tokens"""
    
    # Use model-specific token counting
    tokens = count_tokens(html_content, model)
    print(f"Total tokens for input: {tokens}")
    
    # Use appropriate tokenizer based on model
    if "gemini" in model.lower():
        try:
            gemini_model = TextGenerationModel(model_name=model)
            encoder = gemini_model
        except:
            # Fallback to approximate counting for Gemini
            def encode(text):
                return [1] * (len(text) // 4)  # Approximate tokens
            encoder.encode = encode
    else:
        try:
            encoder = tiktoken.encoding_for_model(model)
        except KeyError:
            encoder = tiktoken.get_encoding("cl100k_base")
            
with open('Web_Page_Class_and_Tests_2/html_links/www.selenium.dev.html', 'r', encoding='utf-8') as file:
    html_content = file.read() 
    
chunks = split_html_by_tokens(html_content)