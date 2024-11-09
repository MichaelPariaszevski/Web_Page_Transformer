from langchain_openai import ChatOpenAI
from langchain.chains import LLMChain
from langchain.prompts import ChatPromptTemplate
from langchain_text_splitters import Language, RecursiveCharacterTextSplitter
from langchain_groq import ChatGroq
from bs4 import BeautifulSoup
from Web_Page_Class_and_Tests_2.Web_Page_Prompt_Templates.Chunks import template_chunks
import asyncio
import time 
import math
import tiktoken

start = time.time()

def split_html_max_30(html_string):
    # Parse HTML
    soup = BeautifulSoup(html_string, 'html.parser')
    
    # Get all elements
    elements = list(soup.descendants)
    total_size = len(html_string)
    
    # Calculate target size per chunk (with some overhead)
    target_chunk_size = math.ceil(total_size / 30)
    
    chunks = []
    current_chunk = ""
    current_size = 0
    
    for element in elements:
        element_str = str(element)
        element_size = len(element_str)
        
        # If adding this element would exceed target size and we haven't hit max chunks
        if current_size + element_size > target_chunk_size and len(chunks) < 29:
            chunks.append(current_chunk)
            current_chunk = element_str
            current_size = element_size
        else:
            current_chunk += element_str
            current_size += element_size
    
    # Add the final chunk
    if current_chunk:
        chunks.append(current_chunk)
    
    # Merge remaining chunks if we have more than 10
    while len(chunks) > 30:
        chunks[-2] += chunks[-1]
        chunks.pop()
        
    return chunks

def split_html(html_content, max_chunk_size=100):
    soup = BeautifulSoup(html_content, 'html.parser')
    chunks = []
    current_chunk = ''
    current_size = 0

    # Iterate over direct children of the body
    for element in soup.body.contents:
        html_string = str(element)
        element_size = len(html_string)

        if current_size + element_size > max_chunk_size and current_chunk:
            chunks.append(current_chunk)
            current_chunk = ''
            current_size = 0

        current_chunk += html_string
        current_size += element_size

    if current_chunk:
        chunks.append(current_chunk)

    return chunks

def html_splitter_langchain(html_content): 
    html_splitter = RecursiveCharacterTextSplitter.from_language(language = Language.HTML, chunk_size = 50000, chunk_overlap = 0)
    html_chunks = html_splitter.create_documents([html_content])
    return html_chunks

# Create prompt template for HTML processing
prompt = ChatPromptTemplate.from_template(template = template_chunks)

# Initialize the chain
llm = ChatOpenAI(model = "gpt-4o-mini", temperature = 0)
llm_groq = ChatGroq(model = "llama-3.2-90b-vision-preview", temperature = 0)
chain = prompt | llm_groq

def count_tokens(text: str, model: str = "gpt-4o-mini") -> int:
    """Count tokens for text using specified model's tokenizer"""
    try:
        encoder = tiktoken.encoding_for_model(model)
        return len(encoder.encode(text))
    except KeyError:
        # Fallback to cl100k_base encoding if model not found
        encoder = tiktoken.get_encoding("cl100k_base")
        return len(encoder.encode(text))

# Synchronous batch processing
def process_html_sync(html_content):
    chunks = split_html(html_content)
    print(len(chunks))
    chunk_list = [{"original_html_code_chunks": chunk} for chunk in chunks]
    # Process all chunks in parallel
    results = chain.batch(inputs = chunk_list)
    return results

def process_html_sync_2(html_content):
    chunks = html_splitter_langchain(html_content)
    print(len(chunks))
    chunk_list = [{"original_html_code_chunks": chunk.page_content} for chunk in chunks]
    # Process all chunks in parallel
    results = chain.batch(inputs = chunk_list)
    return results 

def process_html_sync_3(html_content):
    chunks = split_html_max_30(html_content)
    print(len(chunks))
    for i in chunks: 
        print(len(i))
    chunk_list = [{"original_html_code_chunks": chunk} for chunk in chunks]
    # Process all chunks in parallel
    results = chain.batch(inputs = chunk_list)
    return results

# Asynchronous batch processing
async def process_html_async(html_content):
    chunks = split_html(html_content)
    # Process all chunks in parallel asynchronously
    results = await chain.abatch(
        [{"original_html_code_chunks": chunk} for chunk in chunks]
    )
    return results

# Example usage
with open('Web_Page_Class_and_Tests_2/html_links/www.selenium.dev.html', 'r', encoding='utf-8') as file:
    html_content = file.read()

chunks = split_html_max_30(html_content)

for i in chunks: 
    token_amount = count_tokens(i)
    print(token_amount)

# Sync
# results = process_html_sync_3(html_content)

# print(len(results))

# Async
# async def main():
#     results = await process_html_async(html_content)

# asyncio.run(main())

print(time.time() - start)