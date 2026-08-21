import json
import os

import httpx
from dotenv import load_dotenv

load_dotenv()

question = "How would you build the tallest building ever?"

url = "https://openrouter.ai/api/v1/chat/completions"
headers = {
    "Authorization": f"Bearer {os.getenv("OPEN_ROUTER_KEY")}",
    "Content-Type": "application/json"
}

payload = {
    "model": "openai/gpt-oss-20b",
    "messages": [{"role": "user", "content": question}],
    "stream": True
}

buffer = ""
with httpx.stream("POST", url, headers=headers, json=payload) as r:
    for chunk in r.iter_text():
        buffer += chunk
        print(f"--->{buffer}")
        while True:
            try:
                line_end = buffer.find('\n')
                print(f"--> line_end {line_end}")
                if line_end == -1:
                    break

                line = buffer[:line_end].strip()
                buffer = buffer[line_end + 1:]

                # Skip SSE comments like ": OPENROUTER PROCESSING"
                if line.startswith(':'):
                    continue

                if line.startswith('data: '):
                    data = line[6:]
                    if data == '[DONE]':
                        break

                    try:
                        data_obj = json.loads(data)
                        content = data_obj["choices"][0]["delta"].get("content")
                        # if content:
                        #     print(content, end="", flush=True)
                    except json.JSONDecodeError:
                        pass
            except Exception:
                break

# import httpx
# import json
# from dotenv import load_dotenv
# import os

# load_dotenv()

# response = httpx.get(
#   url="https://openrouter.ai/api/v1/key",
#   headers={
#     "Authorization": f"Bearer {os.getenv("OPEN_ROUTER_KEY")}"
#   }
# )

# print(json.dumps(response.json(), indent=2))