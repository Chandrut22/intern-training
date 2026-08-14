import os

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

messages = [
    {
        "role": "user",
        "content": "What is your cutoff knowledge ?",
    }
]


# First request
response = httpx.post(
    URL,
    headers=HEADERS,
    json={"model": MODEL, "messages": messages},
)

response.raise_for_status()

data = response.json()

message = data["choices"][0]["message"]

print("\nFirst response:")
print(message)


# User asks a follow-up
messages = [
    {
        "role": "user",
        "content": "What major features were introduced in Python 3.14 and can you provide code examples for each?",
    }
]

# Second request
response2 = httpx.post(
    URL,
    headers=HEADERS,
    json={
        "model": MODEL,
        "messages": messages,
    },
)

response2.raise_for_status()

data2 = response2.json()

print("\nSecond response:")
print(data2["choices"][0]["message"])


# User asks a follow-up
messages = [
    {
        "role": "user",
        "content": "who is the CEO of Zoho now ?",
    }
]


# Second request
response3 = httpx.post(
    URL,
    headers=HEADERS,
    json={
        "model": MODEL,
        "messages": messages,
    },
)

response3.raise_for_status()

data3 = response3.json()

print("\nThird response:")
print(data3["choices"][0]["message"])


messages = [
    {
        "role": "user",
        "content": "who is the CEO of Zoho now ?",
    },
    {
        "role": "assistant",
        "content": data3["choices"][0]["message"]["content"],
        "reasoning_details": data3["choices"][0]["message"].get("reasoning_details"),
    },
    {
        "role": "user",
        "content": "Give me the source for this information",
    },
]

response4 = httpx.post(
    URL,
    headers=HEADERS,
    json={
        "model": MODEL,
        "messages": messages,
        "reasoning": {"enabled": True},
    },
)

response4.raise_for_status()

data4 = response4.json()

print("\nFourth response:")
print(data4["choices"][0]["message"])
