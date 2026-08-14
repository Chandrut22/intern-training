import os
import json

import httpx
from dotenv import load_dotenv

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

content = ""

with open("large_prompt.txt", "r", encoding="utf-8") as f:
    content = f.read()

print(len(content))

messages = [
    {
        "role": "user",
        "content": content,
    }
]

# First request
response = httpx.post(
    URL,
    headers=HEADERS,
    json={
        "temperature": 1.0,
        "model": MODEL,
        "messages": messages,
        "max_completion_tokens": 1000,
    },
    timeout=60,
)

response.raise_for_status()

data = response.json()

with open("data.json", "w", encoding="utf-8") as file:
    json.dump(data, file, indent=4)

message = data["choices"][0]["message"]["content"]

print("\nFirst response:")
print(message)

output_path = "chat_output_max_contest.md"
with open(output_path, "a+", encoding="utf-8") as file:
    file.write(message)
