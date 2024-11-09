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
import webbrowser
from dotenv import load_dotenv, find_dotenv 

load_dotenv(find_dotenv(), override = True) 

start = time.time()

prompt = ChatPromptTemplate.from_template(template = template_chunks)

# Initialize the chain
llm = ChatOpenAI(model = "gpt-4o-mini", temperature = 0)
llm_groq = ChatGroq(model = "llama-3.2-90b-vision-preview", temperature = 0)
llm_gemini = ChatGoogleGenerativeAI(model = "gemini-1.5-pro-002")
chain = prompt | llm_gemini

def count_tokens(text: str, model: str = "gemini-1.5-pro-002") -> int:
    """Count tokens for text using specified model's tokenizer"""
    try:
        encoder = tiktoken.encoding_for_model(model)
        return len(encoder.encode(text))
    except KeyError:
        # Fallback to cl100k_base encoding if model not found
        encoder = tiktoken.get_encoding("cl100k_base")
        return len(encoder.encode(text))

def split_html_by_tokens(html_content: str, max_tokens: int = 80000, model: str = "gemini-1.5-pro-002") -> list:
    """Split HTML content into chunks that don't exceed max_tokens"""
    
    try:
        encoder = tiktoken.encoding_for_model(model)
    except KeyError:
        encoder = tiktoken.get_encoding("cl100k_base")
    
    soup = BeautifulSoup(html_content, 'html.parser')
    chunks = []
    current_chunk = ""
    current_tokens = 0
    
    def add_to_chunks(content: str) -> None:
        """Helper function to add content to chunks while respecting token limit"""
        nonlocal current_chunk, current_tokens
        
        # If content itself exceeds max_tokens, split it further
        content_tokens = len(encoder.encode(content))
        if content_tokens > max_tokens:
            # Split into smaller pieces based on characters first
            approx_chars = int((max_tokens / content_tokens) * len(content))
            pieces = [content[i:i + approx_chars] for i in range(0, len(content), approx_chars)]
            
            for piece in pieces:
                piece_tokens = len(encoder.encode(piece))
                if piece_tokens <= max_tokens:
                    chunks.append(piece)
                    print(f"Split piece added: {piece_tokens} tokens")
        else:
            # Check if adding would exceed limit
            if current_tokens + content_tokens > max_tokens:
                if current_chunk:
                    chunks.append(current_chunk)
                    print(f"Chunk created with {current_tokens} tokens")
                current_chunk = content
                current_tokens = content_tokens
            else:
                current_chunk += content
                current_tokens += content_tokens
    
    # Process each element
    for element in soup.body.descendants:
        if isinstance(element, str) and element.strip():
            add_to_chunks(element)
        elif element.name in ['p', 'div', 'section', 'article', 'span', 'li', 'td']:
            element_str = str(element)
            add_to_chunks(element_str)
    
    # Add final chunk
    if current_chunk:
        chunks.append(current_chunk)
        print(f"Final chunk created with {current_tokens} tokens")
    
    # Validate final chunks
    final_chunks = []
    for chunk in chunks:
        chunk_tokens = len(encoder.encode(chunk))
        if chunk_tokens > max_tokens:
            # Split oversized chunks
            temp = chunk
            while temp:
                for i in range(len(temp)):
                    if len(encoder.encode(temp[:i+1])) > max_tokens:
                        final_chunks.append(temp[:i])
                        temp = temp[i:]
                        break
                if len(encoder.encode(temp)) <= max_tokens:
                    final_chunks.append(temp)
                    break
        else:
            final_chunks.append(chunk)
    
    return final_chunks

# Example usage:
def process_html_with_token_limit(html_content: str, rpm: int = 20):
    """Process HTML content with rate limiting for Groq API"""
    chunks = split_html_by_tokens(html_content, max_tokens=80000)
    results = []
    
    # Calculate timing parameters
    delay_between_requests = 60.0 / rpm  # seconds between requests
    batch_size = rpm  # max requests per batch
    
    # Process chunks in batches
    for i in range(0, len(chunks), batch_size):
        batch = chunks[i:i + batch_size]
        batch_start_time = time.time()
        
        # Process current batch
        chunk_list = [{"original_html_code_chunks": chunk} for chunk in batch]
        try:
            batch_results = chain.batch(inputs=chunk_list)
            results.extend(batch_results)
            
            # Log progress
            print(f"Processed batch {i//batch_size + 1}/{math.ceil(len(chunks)/batch_size)}")
            
            # Calculate and apply rate limiting delay
            batch_duration = time.time() - batch_start_time
            required_delay = len(batch) * delay_between_requests
            if batch_duration < required_delay:
                sleep_time = required_delay - batch_duration
                print(f"Rate limiting: sleeping for {sleep_time:.2f} seconds")
                time.sleep(sleep_time)
                
        except Exception as e:
            print(f"Error processing batch: {e}")
            # Add exponential backoff here if needed
            time.sleep(delay_between_requests * 2)
    
    return results

with open('Web_Page_Class_and_Tests_2/html_links/www.apple.com.html', 'r', encoding='utf-8') as file:
    html_content = file.read()

output = process_html_with_token_limit(html_content, rpm = 20) 

print(output)

with open("example_apple.html", "w") as file: 
    output_string = "".join([i.content for i in output])
    file.write(output_string)

print(time.time() - start)

webbrowser.open("example_apple.html")
