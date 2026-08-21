import json
import os

import httpx
from dotenv import load_dotenv
from pydantic import BaseModel, ValidationError

load_dotenv()

class Article(BaseModel):
    title: str
    author: str
    year: int
    summary: str

SCHEMA = {
    "type": "object",
    "properties": {
        "title":   {"type": "string", "description": "Article title"},
        "author":  {"type": "string", "description": "Author full name"},
        "year":    {"type": "integer", "description": "Publication year"},
        "summary": {"type": "string", "description": "One-sentence summary"},
    },
    "required": ["title", "author", "year", "summary"],
    "additionalProperties": False,
}

API_KEY = os.getenv("OPEN_ROUTER_KEY")
MODEL   = "openai/gpt-oss-20b"

def call_openrouter(messages: list[dict]) -> str:
    with httpx.Client() as client:
        resp = client.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {API_KEY}",
                "Content-Type": "application/json",
            },
            json={
                "model": MODEL,
                "messages": messages,
                "response_format": {
                    "type": "json_schema",
                    "json_schema": {
                        "name": "Article",
                        "strict": True,
                        "schema": SCHEMA,
                    },
                },

                # server-side plugin It automatically repairs malformed JSON so you don't have to handle it client-side
                "plugins": [{"id": "response-healing"}],

                # It automatically repairs malformed JSON so you don't have to handle it client-side
                # Non-streaming only — it won't work if you use stream: true
                # Cannot fix truncation — if the response was cut off by max_tokens, healing can't repair it (which is exactly why the manual retry loop is still needed)
             },
        )
        resp.raise_for_status()

        with open("data.json",mode="w") as f:
            json.dump(resp.json(),f,indent=4)

        return resp.json()["choices"][0]["message"]["content"]

def extract_and_validate(raw: str) -> Article:
    data = json.loads(raw)  
    return Article(**data)            

def parse_article(user_text: str) -> Article:
    system_msg = {
        "role": "system",
        "content": (
            "Extract article metadata from the user's text. "
            "Respond ONLY with a valid JSON object matching this schema:\n"
            f"{json.dumps(SCHEMA, indent=2)}"
        ),
    }
    user_msg = {"role": "user", "content": user_text}
    messages = [system_msg, user_msg]

    raw = call_openrouter(messages)
    try:
        return extract_and_validate(raw)
    except (json.JSONDecodeError, ValueError, ValidationError) as e:
        error_detail = str(e)
        print(f"[Attempt failed] {error_detail}\nRaw response:\n{raw}\n")

prompt = """
    I was reading this fascinating piece the other day.
    It was written by Jane Smith back in 2021 and titled
    "The Future of Open-Weight Models". Really insightful stuff
    about how smaller models are closing the gap with proprietary ones.
    """
article = parse_article(prompt)
print(article.model_dump_json(indent=2))