import asyncio
import os
import time
from pathlib import Path

import httpx
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("OPEN_ROUTER_KEY")

if not API_KEY:
    raise RuntimeError("OPEN_ROUTER_KEY is not configured")

URL = "https://openrouter.ai/api/v1/chat/completions"
TIMEOUT = 120.0
OUTPUT_DIR = Path("responses")

MODELS = [
    "openai/gpt-oss-20b",
    "dots-studio/dots-3-note-preview:free",
    "poolside/laguna-xs-2.1:free",
    "sao10k/l3-lunaris-8b",
]

HEADERS = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json",
}


def load_prompts() -> list[str]:
    prompt_file = Path("prompts.txt")

    if not prompt_file.exists():
        raise FileNotFoundError("prompts.txt not found")

    return [
        line.strip()
        for line in prompt_file.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]


def safe_filename(model: str) -> str:
    return model.replace("/", "_").replace(":", "_")


async def fetch(
    client: httpx.AsyncClient,
    model: str,
    prompt: str,
    prompt_index: int,
):
    payload = {
        "model": model,
        "messages": [
            {
                "role": "user",
                "content": prompt,
            }
        ],
    }

    start_time = time.perf_counter()

    try:
        response = await client.post(
            URL,
            headers=HEADERS,
            json=payload,
        )

        latency = time.perf_counter() - start_time

        response.raise_for_status()

        data = response.json()
        content = data["choices"][0]["message"]["content"]

        usage = data.get("usage", {})
        cost = usage.get("cost", 0.0)

        return {
            "prompt_index": prompt_index,
            "prompt": prompt,
            "content": content,
            "latency": latency,
            "cost": cost,
            "error": None,
        }

    except httpx.HTTPStatusError as exc:
        latency = time.perf_counter() - start_time

        return {
            "prompt_index": prompt_index,
            "prompt": prompt,
            "content": None,
            "latency": latency,
            "cost": 0.0,
            "error": f"HTTP {exc.response.status_code}: {exc.response.text}",
        }

    except httpx.RequestError as exc:
        latency = time.perf_counter() - start_time

        return {
            "prompt_index": prompt_index,
            "prompt": prompt,
            "content": None,
            "latency": latency,
            "cost": 0.0,
            "error": str(exc),
        }

    except Exception as exc:
        latency = time.perf_counter() - start_time

        return {
            "prompt_index": prompt_index,
            "prompt": prompt,
            "content": None,
            "latency": latency,
            "cost": 0.0,
            "error": str(exc),
        }


async def process_model(
    client: httpx.AsyncClient,
    model: str,
    prompts: list[str],
):
    tasks = [
        fetch(client, model, prompt, index)
        for index, prompt in enumerate(prompts, start=1)
    ]

    results = await asyncio.gather(*tasks)

    results.sort(key=lambda result: result["prompt_index"])

    output = []

    for result in results:
        prompt_index = result["prompt_index"]
        prompt = result["prompt"]
        content = result["content"]
        error = result["error"]

        output.append(f"# Prompt {prompt_index}\n\n")
        output.append(f"**Prompt:** {prompt}\n\n")

        if error:
            output.append(f"**Error:** {error}\n\n")
        else:
            output.append(f"**Response:**\n\n{content}\n\n")

        output.append(f"**Latency:** {result['latency']:.3f}s\n\n")

        output.append(f"**Cost:** ${result['cost']:.8f}\n\n")

        output.append("---\n\n")

        status = "SUCCESS" if content else "ERROR"

        print(
            f"[{status}] "
            f"model={model} "
            f"prompt={prompt_index} "
            f"latency={result['latency']:.3f}s "
            f"cost=${result['cost']:.8f}"
        )

    filename = OUTPUT_DIR / f"{safe_filename(model)}.md"

    filename.write_text(
        "".join(output),
        encoding="utf-8",
    )

    total_cost = sum(result["cost"] for result in results)
    successful_results = [result for result in results if result["content"]]

    if successful_results:
        avg_latency = sum(result["latency"] for result in successful_results) / len(
            successful_results
        )
    else:
        avg_latency = 0.0

    if successful_results:
        avg_cost = total_cost / len(successful_results)
    else:
        avg_cost = 0.0

    return {
        "model": model,
        "avg_cost": avg_cost,
        "total_cost": total_cost,
        "avg_latency": avg_latency,
        "successful_calls": len(successful_results),
        "total_calls": len(results),
    }


def create_comparison(results: list[dict]) -> None:
    output = [
        "# Model Comparison\n\n",
        "| Model | Avg Cost / Call | Total Cost | Avg Latency | Successful Calls | Usable |\n",
        "|---|---:|---:|---:|---:|---|\n",
    ]

    for result in results:
        output.append(
            f"| {result['model']} "
            f"| ${result['avg_cost']:.8f} "
            f"| ${result['total_cost']:.8f} "
            f"| {result['avg_latency']:.3f}s "
            f"| {result['successful_calls']}/{result['total_calls']} "
        )

    filename = OUTPUT_DIR / "comparison.md"

    filename.write_text("".join(output), encoding="utf-8")

    print(f"[SAVED] {filename}")


async def main():
    prompts = load_prompts()

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    async with httpx.AsyncClient(timeout=TIMEOUT) as client:
        tasks = [process_model(client, model, prompts) for model in MODELS]

        results = await asyncio.gather(*tasks)

    create_comparison(results)


if __name__ == "__main__":
    asyncio.run(main())
