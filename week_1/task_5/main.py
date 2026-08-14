import asyncio
import os
import time
from dataclasses import dataclass
from typing import Any

import httpx
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("OPEN_ROUTER_KEY")
if not API_KEY:
    raise RuntimeError("OPEN_ROUTER_KEY is not configured")

URL = "https://openrouter.ai/api/v1/chat/completions"
MODEL = "openai/gpt-oss-20b"
TIMEOUT = 120.0

HEADERS = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json",
}

PROMPTS = []

with open("prompt.txt", "r", encoding="utf-8") as file:
    for line in file:
        PROMPTS.append(line)


@dataclass
class RequestResult:
    index: int
    success: bool
    latency: float
    input_tokens: int = 0
    output_tokens: int = 0
    total_tokens: int = 0
    cost: float = 0.0
    error: str | None = None


async def send_request(
    client: httpx.AsyncClient,
    prompt: str,
    index: int,
) -> RequestResult:

    payload = {
        "model": MODEL,
        "messages": [{"role": "user", "content": prompt}],
        "max_tokens": 200,
        "temperature": 0,
    }

    start = time.perf_counter()

    try:
        response = await client.post(URL, headers=HEADERS, json=payload)
        latency = time.perf_counter() - start
        response.raise_for_status()

        data: dict[str, Any] = response.json()
        usage = data.get("usage", {})

        input_tokens = usage.get("prompt_tokens", 0)
        output_tokens = usage.get("completion_tokens", 0)
        total_tokens = usage.get("total_tokens", input_tokens + output_tokens)
        cost = usage.get("cost")

        print(
            f"[{index + 1}] SUCCESS | time={latency:.2f}s | input={input_tokens} | output={output_tokens} | total={total_tokens} | cost=${cost:.6f}"
        )

        return RequestResult(
            index=index,
            success=True,
            latency=latency,
            input_tokens=input_tokens,
            output_tokens=output_tokens,
            total_tokens=total_tokens,
            cost=cost,
        )

    except httpx.HTTPStatusError as exc:
        latency = time.perf_counter() - start
        error = f"HTTP {exc.response.status_code}: {exc.response.text[:200]}"

        print(f"[{index + 1}] FAILED | time={latency:.2f}s | error={error}")

        return RequestResult(
            index=index,
            success=False,
            latency=latency,
            error=error,
        )

    except Exception as exc:
        latency = time.perf_counter() - start
        error = str(exc)

        print(f"[{index + 1}] FAILED | time={latency:.2f}s | error={error}")

        return RequestResult(
            index=index,
            success=False,
            latency=latency,
            error=error,
        )


async def sequential_test(prompts: list[str]) -> tuple[list[RequestResult], float]:
    print("\nSEQUENTIAL TEST")

    async with httpx.AsyncClient(timeout=TIMEOUT) as client:
        start = time.perf_counter()

        results = []

        for index, prompt in enumerate(prompts):
            result = await send_request(client, prompt, index)
            results.append(result)

        total_time = time.perf_counter() - start

    print(f"Sequential | requests={len(prompts)} | time={total_time:.2f}s")

    return results, total_time


async def concurrent_test(prompts: list[str]) -> tuple[list[RequestResult], float]:
    print("\nCONCURRENT TEST")

    async with httpx.AsyncClient(timeout=TIMEOUT) as client:
        start = time.perf_counter()

        tasks = [
            send_request(client, prompt, index) for index, prompt in enumerate(prompts)
        ]

        results = await asyncio.gather(*tasks)

        total_time = time.perf_counter() - start

    print(f"Concurrent | requests={len(prompts)} | time={total_time:.2f}s")

    return results, total_time


def get_stats(results: list[RequestResult]) -> dict[str, Any]:
    successful = sum(result.success for result in results)
    failed = len(results) - successful

    input_tokens = sum(result.input_tokens for result in results)
    output_tokens = sum(result.output_tokens for result in results)
    total_tokens = sum(result.total_tokens for result in results)
    total_cost = sum(result.cost for result in results)

    average_latency = (
        sum(result.latency for result in results) / len(results) if results else 0
    )

    return {
        "requests": len(results),
        "successful": successful,
        "failed": failed,
        "input_tokens": input_tokens,
        "output_tokens": output_tokens,
        "total_tokens": total_tokens,
        "cost": total_cost,
        "average_latency": average_latency,
    }


async def main() -> None:
    print(f"MODEL={MODEL}")
    print(f"BATCH_SIZE={len(PROMPTS)}")

    sequential_results, sequential_time = await sequential_test(PROMPTS)
    concurrent_results, concurrent_time = await concurrent_test(PROMPTS)

    sequential = get_stats(sequential_results)
    concurrent = get_stats(concurrent_results)

    speedup = sequential_time / concurrent_time if concurrent_time > 0 else 0

    time_saved = sequential_time - concurrent_time

    improvement = time_saved / sequential_time * 100 if sequential_time > 0 else 0

    print("\nRESULT")
    print(
        f"Sequential | requests={sequential['requests']} | success={sequential['successful']} | failed={sequential['failed']} | time={sequential_time:.2f}s | avg_latency={sequential['average_latency']:.2f}s | input_tokens={sequential['input_tokens']} | output_tokens={sequential['output_tokens']} | total_tokens={sequential['total_tokens']} | cost=${sequential['cost']:.6f} | throughput={sequential['successful'] / sequential_time:.2f} req/s"
    )
    print(
        f"Concurrent | requests={concurrent['requests']} | success={concurrent['successful']} | failed={concurrent['failed']} | time={concurrent_time:.2f}s | avg_latency={concurrent['average_latency']:.2f}s | input_tokens={concurrent['input_tokens']} | output_tokens={concurrent['output_tokens']} | total_tokens={concurrent['total_tokens']} | cost=${concurrent['cost']:.6f} | throughput={concurrent['successful'] / concurrent_time:.2f} req/s"
    )
    print(
        f"Comparison | time_saved={time_saved:.2f}s | speedup={speedup:.2f}x | improvement={improvement:.2f}% | cost_difference=${concurrent['cost'] - sequential['cost']:.6f}"
    )


if __name__ == "__main__":
    asyncio.run(main())
