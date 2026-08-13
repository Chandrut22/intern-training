import json
import logging
import os
import time

import httpx
from dotenv import load_dotenv
from transformers import AutoTokenizer

load_dotenv()

API_KEY = os.getenv("OPEN_ROUTER_KEY")

if not API_KEY:
    raise RuntimeError("OPEN_ROUTER_KEY is not configured")

URL = "https://openrouter.ai/api/v1/chat/completions"

HEADERS = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json",
}

MODEL = "openai/gpt-oss-20b"
USD_TO_INR = 95.4

INPUT_PRICE_PER_1M = 0.03
OUTPUT_PRICE_PER_1M = 0.13

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
)

logger = logging.getLogger(__name__)

TOKENIZER = AutoTokenizer.from_pretrained("openai/gpt-oss-20b")


def count_tokens(messages: list[dict]) -> int:
    tokenized = TOKENIZER.apply_chat_template(
        messages,
        tokenize=True,
        add_generation_prompt=True,
        return_tensors=None,
    )
    print(tokenized)
    return len(tokenized['input_ids'])


def calculate_cost(
    prompt_tokens: int,
    completion_tokens: int,
    input_price_per_1m: float,
    output_price_per_1m: float,
) -> tuple[float, float, float]:
    input_cost = (prompt_tokens / 1_000_000) * input_price_per_1m
    output_cost = (completion_tokens / 1_000_000) * output_price_per_1m
    total_cost = input_cost + output_cost
    return input_cost, output_cost, total_cost


messages = [
    {
        "role": "user",
        "content": "What is your cutoff knowledge?",
    }
]

prompt = {
    "model": MODEL,
    "messages": messages,
}

estimated_prompt_tokens = count_tokens(messages)

logger.info("Estimated prompt tokens (pre-flight): %d",estimated_prompt_tokens)

start_time = time.perf_counter()

response = httpx.post(
    URL,
    headers=HEADERS,
    json=prompt,
    timeout=60.0,
)

end_time = time.perf_counter()

latency_ms = (end_time - start_time) * 1000

response.raise_for_status()

data = response.json()

with open("data.json", "w", encoding="utf-8") as file:
    json.dump(data, file, indent=4)

message = data["choices"][0]["message"]

usage = data.get("usage", {})

prompt_tokens = usage.get("prompt_tokens", 0)
completion_tokens = usage.get("completion_tokens", 0)
total_tokens = usage.get("total_tokens", 0)

response_cost_usd = usage.get("cost")

input_cost_usd, output_cost_usd, total_cost_usd = calculate_cost(
    prompt_tokens=prompt_tokens,
    completion_tokens=completion_tokens,
    input_price_per_1m=INPUT_PRICE_PER_1M,
    output_price_per_1m=OUTPUT_PRICE_PER_1M,
)

total_cost_inr = total_cost_usd * USD_TO_INR

response_cost_inr = (
    response_cost_usd * USD_TO_INR
    if response_cost_usd is not None
    else None
)

logger.info("Model:                             %s", MODEL)
logger.info("Model provider:                    %s", data.get("provider"))
logger.info("Pre-flight estimated tokens:       %d", estimated_prompt_tokens)
logger.info("OpenRouter prompt tokens:          %d", prompt_tokens)
logger.info("Completion tokens:                 %d", completion_tokens)
logger.info("Total tokens:                      %d", total_tokens)

logger.info("Response cost from OpenRouter:     $%.10f", response_cost_usd)
logger.info("Response cost from OpenRouter:     ₹%.10f", response_cost_inr)

logger.info("Calculated Input cost:             $%.10f", input_cost_usd)
logger.info("Calculated Output cost:            $%.10f", output_cost_usd)
logger.info("Calculated Total cost:             $%.10f", total_cost_usd)
logger.info("Calculated Total cost:             ₹%.10f", total_cost_inr)

logger.info("Latency:                           %.2f ms", latency_ms)
logger.info("Model response: %s", message["content"])