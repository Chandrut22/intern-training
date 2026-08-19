import httpx
from dotenv import load_dotenv
import json
import os

load_dotenv()

prompt = """give the program to chat to the llm in openrouter as API request using httpx 
                and need to implement the async and i need to stream the llm
                and  user give the input prompt and print the token usage, cost, model name for every chat
            """

response = httpx.post(
    "https://openrouter.ai/api/v1/chat/completions",
    headers={
        "Authorization": f"Bearer {os.getenv("OPEN_ROUTER_KEY")}",
        "Content-Type": "application/json",
    },
    json={
        "model": "openai/gpt-oss-20b",
        "messages": [
            {"role": "user", "content": prompt}
        ],
        "reasoning": {
            "effort": "medium"   # "high", "medium", "low"
            # "max_tokens": 2000
            # "exclude": True  # hide reasoning from response
        }
    }
)

response.raise_for_status()

data = response.json()
msg = data["choices"][0]["message"]
print("REASONING:", msg.get("reasoning"))
print("CONTENT:", msg.get("content"))

with open("data.json",mode="w") as file:
    json.dump(data,file,indent=4)

with open("response_v5.md", mode="w",encoding="utf-8") as file:
    file.write(f"\n# Prompt: {prompt}\n\n## Response:\n{msg.get("content")}\n\n## Reasoning:\n{msg.get("content")}\n")