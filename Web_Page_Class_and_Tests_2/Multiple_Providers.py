import asyncio
from typing import List, Dict, Any
from dataclasses import dataclass
from langchain_openai import ChatOpenAI
from langchain_groq import ChatGroq
from langchain.prompts import ChatPromptTemplate
from Web_Page_Class_and_Tests_2.Web_Page_Prompt_Templates.Chunks import template_chunks
from Web_Page_Class_and_Tests_2.Web_Page_Test_Py_2 import split_html_by_tokens
import os
from concurrent.futures import ThreadPoolExecutor

@dataclass
class LLMConfig:
    name: str
    model: str
    api_key: str
    rpm: int

class MultiProviderProcessor:
    def __init__(self, providers: List[LLMConfig], template: str):
        self.providers = {}
        for provider in providers:
            if provider.name == "openai":
                llm = ChatOpenAI(
                    model=provider.model,
                    openai_api_key=provider.api_key,
                    temperature=0
                )
            elif provider.name == "groq":
                llm = ChatGroq(
                    model=provider.model,
                    groq_api_key=provider.api_key,
                    temperature=0
                )
            
            self.providers[provider.name] = {
                "llm": llm,
                "chain": ChatPromptTemplate.from_template(template) | llm,
                "rpm": provider.rpm
            }

    async def process_chunk_with_provider(
        self, 
        chunk: str, 
        provider_name: str,
        semaphore: asyncio.Semaphore
    ) -> Dict[str, Any]:
        provider = self.providers[provider_name]
        delay = 60.0 / provider["rpm"]
        
        async with semaphore:
            try:
                result = await provider["chain"].ainvoke(
                    {"original_html_code_chunks": chunk}
                )
                await asyncio.sleep(delay)
                return {"result": result, "provider": provider_name}
            except Exception as e:
                print(f"Error with {provider_name}: {e}")
                return {"error": str(e), "provider": provider_name}

    async def process_chunks(
        self, 
        chunks: List[str],
        distribution: Dict[str, float] = {"openai": 0.7, "groq": 0.3}
    ):
        # Distribute chunks between providers
        total_chunks = len(chunks)
        provider_chunks = {}
        current_idx = 0
        
        for provider, ratio in distribution.items():
            chunk_count = int(total_chunks * ratio)
            provider_chunks[provider] = chunks[current_idx:current_idx + chunk_count]
            current_idx += chunk_count
        
        # Add remaining chunks to last provider
        if current_idx < total_chunks:
            last_provider = list(distribution.keys())[-1]
            provider_chunks[last_provider].extend(chunks[current_idx:])

        # Create semaphores for rate limiting
        semaphores = {
            name: asyncio.Semaphore(config["rpm"])
            for name, config in self.providers.items()
        }

        # Process chunks concurrently
        tasks = []
        for provider_name, provider_chunks in provider_chunks.items():
            for chunk in provider_chunks:
                task = self.process_chunk_with_provider(
                    chunk,
                    provider_name,
                    semaphores[provider_name]
                )
                tasks.append(task)

        results = await asyncio.gather(*tasks)
        return results

# Usage example:
async def main():
    providers = [
        LLMConfig(
            name="openai",
            model="gpt-4o-mini",
            api_key=os.getenv("OPENAI_API_KEY"),
            rpm=3500
        ),
        LLMConfig(
            name="groq",
            model="llama-3.1-70b-instruct",
            api_key=os.getenv("GROQ_API_KEY"),
            rpm=30
        )
    ]

    processor = MultiProviderProcessor(providers, template_chunks)
    
    with open('Web_Page_Class_and_Tests_2/html_links/www.selenium.dev.html', 'r', encoding='utf-8') as file:
        html_content = file.read()
    
    # Get chunks using existing function
    chunks = split_html_by_tokens(html_content, max_tokens=7000)
    
    # Process with multiple providers
    results = await processor.process_chunks(
        chunks,
        distribution={"openai": 0.7, "groq": 0.3}
    )
    return results

# Run the async function
if __name__ == "__main__":
    results = asyncio.run(main())