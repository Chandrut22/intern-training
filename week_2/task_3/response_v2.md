
# Prompt: give the program to chat to the llm in openrouter as API request using httpx

## Response:
Below is a **minimal yet functional** Python script that talks to an LLM hosted on OpenRouter (or any OpenAI‑compatible endpoint) using the `httpx` library.  
The example is written twice – once with the blocking `httpx.Client` and a second time with the async `httpx.AsyncClient`.  
Feel free to copy‑paste one of the blocks into a file called `openrouter_chat.py` and run it.

> **Prerequisites**  
> *Python 3.9+*  
> ```bash
> pip install httpx
> ```  
> *An OpenRouter API key* – store it in an environment variable called `OPENROUTER_API_KEY` (recommended)

```bash
# Linux / macOS
export OPENROUTER_API_KEY="sk-XXXXXXXXXXXXXXXXXXXX"

# Windows CMD
set OPENROUTER_API_KEY=sk-XXXXXXXXXXXXXXXXXXXX

# Windows PowerShell
$env:OPENROUTER_API_KEY="sk-XXXXXXXXXXXXXXXXXXXX"
```

---

## 1️⃣ Blocking (synchronous) version

```python
#!/usr/bin/env python3
"""
Blocking example: httpx + OpenRouter chat endpoint
"""

import os
import json
import httpx

API_KEY = os.getenv("OPENROUTER_API_KEY")
if not API_KEY:
    raise RuntimeError("Please set OPENROUTER_API_KEY")

URL = "https://openrouter.ai/api/v1/chat/completions"

HEADERS = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json",
    # Optional: set an organization ID if you’re using one
    # "OpenAI-Organization": "org-xxxxxxxx",
}

# The payload you send to OpenRouter
PAYLOAD = {
    "model": "meta-llama/Meta-Llama-3.1-8B-Instruct",
    "messages": [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Hello, how can I use HTTPX to call an LLM?"},
    ],
    # These are optional, but nice to have
    "max_tokens": 250,
    "temperature": 0.7,
}

def chat(payload: dict) -> str:
    """
    Send a prompt to OpenRouter and return the assistant’s reply text.
    """
    with httpx.Client() as client:
        response = client.post(URL, headers=HEADERS, json=payload)
        response.raise_for_status()                 # raise if 4xx/5xx
        data = response.json()

        # A typical OpenAI/ChatCompletion response
        message = data["choices"][0]["message"]["content"]
        return message

if __name__ == "__main__":
    reply = chat(PAYLOAD)
    print("Assistant ➜", reply)
```

---

## 2️⃣ Async version

If your application is already async (e.g. FastAPI, aiohttp, etc.) you’ll probably want the async variant.

```python
#!/usr/bin/env python3
"""
Async example: httpx.AsyncClient + OpenRouter chat endpoint
"""

import os
import json
import httpx
import asyncio

API_KEY = os.getenv("OPENROUTER_API_KEY")
if not API_KEY:
    raise RuntimeError("Please set OPENROUTER_API_KEY")

URL = "https://openrouter.ai/api/v1/chat/completions"

HEADERS = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json",
}

PAYLOAD = {
    "model": "meta-llama/Meta-Llama-3.1-8B-Instruct",
    "messages": [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Show me how to iterate over a list in Python."},
    ],
    "max_tokens": 250,
    "temperature": 0.7,
}

async def chat_async(payload: dict) -> str:
    async with httpx.AsyncClient() as client:
        response = await client.post(URL, headers=HEADERS, json=payload)
        response.raise_for_status()
        data = response.json()
        return data["choices"][0]["message"]["content"]

async def main():
    reply = await chat_async(PAYLOAD)
    print("Assistant ➜", reply)

if __name__ == "__main__":
    asyncio.run(main())
```

---

## 3️⃣ Interactive CLI (optional)

If you’d rather have a little REPL that talks back and forth, wrap the async function in a simple loop:

```python
async def prompt_loop():
    while True:
        user = input("You: ")
        if user.strip().lower() in {"quit", "exit"}:
            print("Bye!")
            break
        payload = {
            "model": "meta-llama/Meta-Llama-3.1-8B-Instruct",
            "messages": [
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": user},
            ],
            "max_tokens": 500,
            "temperature": 0.7,
        }
        reply = await chat_async(payload)
        print("Assistant:", reply)

if __name__ == "__main__":
    asyncio.run(prompt_loop())
```

---

### What does the script do?

| Step | What happens |
|------|--------------|
| 1    | Imports `httpx` (blocking or async version) |
| 2    | Retrieves your API key from the environment |
| 3    | Builds the request headers (`Authorization`, `Content-Type`) |
| 4    | Constructs a minimal `messages` list for a chat completion |
| 5    | Sends a `POST` request to `https://openrouter.ai/api/v1/chat/completions` |
| 6    | Checks the HTTP status, parses JSON, and extracts the assistant’s text |
| 7    | Prints the answer to the console |

Feel free to swap out:

* `model`: pick any of the models OpenRouter offers (`meta-llama/Meta-Llama-3.1-8B-Instruct`, `gpt-4o`, etc.)
* `max_tokens`: how long you want the reply to be
* `temperature`: how “creative” you want the model to be
* `top_p`, `frequency_penalty`, `presence_penalty`, etc. – all the usual OpenAI options.

Happy coding! 🚀

## Reasoning:
Below is a **minimal yet functional** Python script that talks to an LLM hosted on OpenRouter (or any OpenAI‑compatible endpoint) using the `httpx` library.  
The example is written twice – once with the blocking `httpx.Client` and a second time with the async `httpx.AsyncClient`.  
Feel free to copy‑paste one of the blocks into a file called `openrouter_chat.py` and run it.

> **Prerequisites**  
> *Python 3.9+*  
> ```bash
> pip install httpx
> ```  
> *An OpenRouter API key* – store it in an environment variable called `OPENROUTER_API_KEY` (recommended)

```bash
# Linux / macOS
export OPENROUTER_API_KEY="sk-XXXXXXXXXXXXXXXXXXXX"

# Windows CMD
set OPENROUTER_API_KEY=sk-XXXXXXXXXXXXXXXXXXXX

# Windows PowerShell
$env:OPENROUTER_API_KEY="sk-XXXXXXXXXXXXXXXXXXXX"
```

---

## 1️⃣ Blocking (synchronous) version

```python
#!/usr/bin/env python3
"""
Blocking example: httpx + OpenRouter chat endpoint
"""

import os
import json
import httpx

API_KEY = os.getenv("OPENROUTER_API_KEY")
if not API_KEY:
    raise RuntimeError("Please set OPENROUTER_API_KEY")

URL = "https://openrouter.ai/api/v1/chat/completions"

HEADERS = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json",
    # Optional: set an organization ID if you’re using one
    # "OpenAI-Organization": "org-xxxxxxxx",
}

# The payload you send to OpenRouter
PAYLOAD = {
    "model": "meta-llama/Meta-Llama-3.1-8B-Instruct",
    "messages": [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Hello, how can I use HTTPX to call an LLM?"},
    ],
    # These are optional, but nice to have
    "max_tokens": 250,
    "temperature": 0.7,
}

def chat(payload: dict) -> str:
    """
    Send a prompt to OpenRouter and return the assistant’s reply text.
    """
    with httpx.Client() as client:
        response = client.post(URL, headers=HEADERS, json=payload)
        response.raise_for_status()                 # raise if 4xx/5xx
        data = response.json()

        # A typical OpenAI/ChatCompletion response
        message = data["choices"][0]["message"]["content"]
        return message

if __name__ == "__main__":
    reply = chat(PAYLOAD)
    print("Assistant ➜", reply)
```

---

## 2️⃣ Async version

If your application is already async (e.g. FastAPI, aiohttp, etc.) you’ll probably want the async variant.

```python
#!/usr/bin/env python3
"""
Async example: httpx.AsyncClient + OpenRouter chat endpoint
"""

import os
import json
import httpx
import asyncio

API_KEY = os.getenv("OPENROUTER_API_KEY")
if not API_KEY:
    raise RuntimeError("Please set OPENROUTER_API_KEY")

URL = "https://openrouter.ai/api/v1/chat/completions"

HEADERS = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json",
}

PAYLOAD = {
    "model": "meta-llama/Meta-Llama-3.1-8B-Instruct",
    "messages": [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Show me how to iterate over a list in Python."},
    ],
    "max_tokens": 250,
    "temperature": 0.7,
}

async def chat_async(payload: dict) -> str:
    async with httpx.AsyncClient() as client:
        response = await client.post(URL, headers=HEADERS, json=payload)
        response.raise_for_status()
        data = response.json()
        return data["choices"][0]["message"]["content"]

async def main():
    reply = await chat_async(PAYLOAD)
    print("Assistant ➜", reply)

if __name__ == "__main__":
    asyncio.run(main())
```

---

## 3️⃣ Interactive CLI (optional)

If you’d rather have a little REPL that talks back and forth, wrap the async function in a simple loop:

```python
async def prompt_loop():
    while True:
        user = input("You: ")
        if user.strip().lower() in {"quit", "exit"}:
            print("Bye!")
            break
        payload = {
            "model": "meta-llama/Meta-Llama-3.1-8B-Instruct",
            "messages": [
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": user},
            ],
            "max_tokens": 500,
            "temperature": 0.7,
        }
        reply = await chat_async(payload)
        print("Assistant:", reply)

if __name__ == "__main__":
    asyncio.run(prompt_loop())
```

---

### What does the script do?

| Step | What happens |
|------|--------------|
| 1    | Imports `httpx` (blocking or async version) |
| 2    | Retrieves your API key from the environment |
| 3    | Builds the request headers (`Authorization`, `Content-Type`) |
| 4    | Constructs a minimal `messages` list for a chat completion |
| 5    | Sends a `POST` request to `https://openrouter.ai/api/v1/chat/completions` |
| 6    | Checks the HTTP status, parses JSON, and extracts the assistant’s text |
| 7    | Prints the answer to the console |

Feel free to swap out:

* `model`: pick any of the models OpenRouter offers (`meta-llama/Meta-Llama-3.1-8B-Instruct`, `gpt-4o`, etc.)
* `max_tokens`: how long you want the reply to be
* `temperature`: how “creative” you want the model to be
* `top_p`, `frequency_penalty`, `presence_penalty`, etc. – all the usual OpenAI options.

Happy coding! 🚀
