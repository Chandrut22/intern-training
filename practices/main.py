import asyncio
import time
import os
from langchain_openrouter import ChatOpenRouter
from langchain_core.prompts import ChatPromptTemplate
from dotenv import load_dotenv

load_dotenv()

async def run_prompt(chain, prompt_text, prompt_index):
    """Runs a single prompt and measures its individual latency."""
    start_time = time.perf_counter()
    
    print(f"[Task {prompt_index}] Started...")
    response = await chain.ainvoke({"prompt": prompt_text})
    
    end_time = time.perf_counter()
    latency = end_time - start_time
    
    print(f"[Task {prompt_index}] Finished in {latency:.2f} seconds.")
    return prompt_index, prompt_text, response.content, latency

async def main():
    model = ChatOpenRouter(model="openai/gpt-oss-20b",api_key=os.getenv("OPEN_ROUTER_KEY"))
    
    prompt_template = ChatPromptTemplate.from_template("{prompt}")
    chain = prompt_template | model

    prompts = [
        "Write a Python httpx script to call an LLM through OpenRouter and return the model's response.",
        "Benchmark a batch of LLM requests using both sequential execution and asyncio.gather(). Show total time, throughput, token usage, and estimated cost.",
        "Generate a prompt larger than a model's 131K-token context window and test how the API handles the request.",
        "Create five test prompts that evaluate whether an LLM hallucinates information about events, people, or facts outside its knowledge cutoff.",
        "Analyze this OpenRouter API error and explain the cause, HTTP status code, and how to fix it."
    ]

    print(f"Starting {len(prompts)} concurrent complex requests...\n")
    total_start_time = time.perf_counter()

    tasks = [run_prompt(chain, prompt_text, idx + 1) for idx, prompt_text in enumerate(prompts)]

    results = await asyncio.gather(*tasks)

    total_end_time = time.perf_counter()
    total_latency = total_end_time - total_start_time

    print("\n" + "="*20 + " RESULTS SUMMARY " + "="*20)
    for idx, original_prompt, response_content, latency in results:
        print(f"\n[PROMPT {idx} - {latency:.2f}s]: {original_prompt}")
        print(f"--- ANSWER ---")
        print(response_content.strip())
        print("-" * 50)

    print(f"\nTotal elapsed time for all {len(prompts)} requests: {total_latency:.2f} seconds.")

if __name__ == "__main__":
    asyncio.run(main())
