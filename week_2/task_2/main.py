import asyncio
import json
import os

import httpx
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("OPEN_ROUTER_KEY")
if not API_KEY:
    raise ValueError("OPEN_ROUTER_KEY not set in .env")

URL = "https://openrouter.ai/api/v1/chat/completions"
HEADERS = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json",
}
MODELS = [
    "openai/gpt-4o",
    "openai/gpt-oss-20b",
]

COMMANDS = {"exit", "quit", "history"}


def print_history(history: list[dict]) -> None:
    if not history:
        print("No history yet.")
        return
    print("\n--- Conversation History ---")
    for i, msg in enumerate(history, 1):
        print(f"[{i}] {msg['role'].capitalize()}: {msg['content']}")
    print("----------------------------")


def print_stats(used_model: str, prompt_tokens: int, completion_tokens: int, turn_cost: float, running_cost: float) -> None:
    print(f"\n[Model: {used_model}]")
    print(f"[Tokens: prompt={prompt_tokens} | completion={completion_tokens} | total={prompt_tokens + completion_tokens}]")
    print(f"[Cost: turn=${turn_cost:.6f} | running=${running_cost:.6f}]")


async def stream_response(client: httpx.AsyncClient,history: list[dict]) -> tuple[str, float, str, int, int]:
    payload = {
        "models": MODELS,
        "messages": history,
        "stream": True,
    }

    assistant_text = ""
    turn_cost = 0.0
    used_model = ""
    prompt_tokens = 0
    completion_tokens = 0

    try:
        async with client.stream("POST", URL, headers=HEADERS, json=payload, timeout=None) as response:
            if response.status_code != 200:
                error_body = await response.aread()
                try:
                    error_msg = json.loads(error_body).get("error", {}).get("message", "Unknown API error")
                except json.JSONDecodeError:
                    error_msg = error_body.decode(errors="replace")
                print(f"\nRequest failed ({response.status_code}): {error_msg}")
                return "", 0.0, "", 0, 0

            async for line in response.aiter_lines():
                if not line.startswith("data: "):
                    continue

                data = line[6:].strip()
                if data == "[DONE]":
                    break

                try:
                    parsed = json.loads(data)
                    with open("data.json","w+") as file:
                        json.dump(parsed,file,indent=4)
                        
                except json.JSONDecodeError:
                    continue

                if "error" in parsed:
                    print(f"\nStream error: {parsed['error'].get('message', 'Unknown stream error')}")
                    return "", 0.0, used_model, prompt_tokens, completion_tokens

                if parsed.get("model"):
                    used_model = parsed["model"]

                usage = parsed.get("usage")
                if usage:
                    turn_cost = usage.get("cost", 0.0)
                    prompt_tokens = usage.get("prompt_tokens", 0)
                    completion_tokens = usage.get("completion_tokens", 0)

                choices = parsed.get("choices", [])
                if not choices:
                    continue

                choice = choices[0]
                if choice.get("finish_reason") == "error":
                    print("\nStream terminated with error.")
                    return "", 0.0, used_model, prompt_tokens, completion_tokens

                content = choice.get("delta", {}).get("content")
                if content:
                    assistant_text += content
                    print(content, end="", flush=True)

    except httpx.HTTPError as exc:
        print(f"\nHTTP error: {exc}")
        return "", 0.0, "", 0, 0

    except Exception as exc:
        print(f"\nUnexpected error: {exc}")
        return "", 0.0, "", 0, 0

    return assistant_text, turn_cost, used_model, prompt_tokens, completion_tokens


async def main() -> None:
    history: list[dict] = []
    running_cost = 0.0

    async with httpx.AsyncClient() as client:
        while True:
            try:
                prompt = input("\nYou: ").strip()
            except (KeyboardInterrupt, EOFError):
                print("\nExiting...")
                break

            if not prompt:
                continue

            command = prompt.lower()

            if command in {"exit", "quit"}:
                print(f"\nTotal spent: ${running_cost:.6f}")
                break

            if command == "history":
                print_history(history)

            history.append({"role": "user", "content": prompt})
            print("Assistant: ", end="", flush=True)

            assistant_text, turn_cost, used_model, prompt_tokens, completion_tokens = (
                await stream_response(client, history)
            )

            print()  # newline after streamed response

            if not assistant_text:
                history.pop()
                continue

            history.append({"role": "assistant", "content": assistant_text})
            running_cost += turn_cost
            print_stats(used_model, prompt_tokens, completion_tokens, turn_cost, running_cost)


if __name__ == "__main__":
    asyncio.run(main())