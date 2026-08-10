import asyncio
import functools
import re
import time
from typing import Generator
from pydantic import BaseModel, ValidationError


def extract_json_from_fences(text: str) -> str:
    """Strips markdown code fences from a block of text and returns the inner JSON."""
    pattern = r"```(?:json)?\s*([\s\S]*?)\s*```"
    match = re.search(pattern, text, re.IGNORECASE)
    return match.group(1).strip() if match else text.strip()


PHONE_REGEX = re.compile(
    r"(?<!\d)(?:\(?\d{3}\)?[\s\-\.]*)\d{3}[\s\-\.]*\d{4}(?!\d)"
)


def redact_phone_numbers(text: str) -> str:
    """Replaces every 10-digit phone number in a block of text with [PHONE]."""
    return PHONE_REGEX.sub("[PHONE]", text)


class Medication(BaseModel):
    name: str
    dose: str | None = None


def calculate_cost(
    prompt_tokens: int, completion_tokens: int, model: str = "gpt-4o"
) -> float:
    """Calculates API cost given token usage counts."""
    rates = {
        "gpt-4o": {"input": 0.0025 / 1000, "output": 0.01 / 1000},
        "gpt-4o-mini": {"input": 0.00015 / 1000, "output": 0.0006 / 1000},
    }
    selected = rates.get(model, rates["gpt-4o"])
    return (prompt_tokens * selected["input"]) + (
        completion_tokens * selected["output"]
    )


def chunk_text(text: str, chunk_size: int = 800) -> Generator[str, None, None]:
    """Yields text in chunks of specified size (default 800 chars)."""
    for i in range(0, len(text), chunk_size):
        yield text[i : i + chunk_size]


async def async_fetch_data(value: int) -> int:
    """Simulates an asynchronous I/O operation taking 1 second."""
    await asyncio.sleep(1.0)
    return value * 2


async def run_twenty_concurrently() -> list[int]:
    """Runs 20 async operations concurrently using asyncio.gather."""
    tasks = [async_fetch_data(i) for i in range(20)]
    return await asyncio.gather(*tasks)


def run_async_benchmarks() -> tuple[float, float]:
    """Times single vs. 20 concurrent operations and prints performance differences."""
    # Sequential 1-second operation
    t0 = time.perf_counter()
    res_single = asyncio.run(async_fetch_data(5))
    time_single = time.perf_counter() - t0

    # 20 Concurrent 1-second operations
    t0 = time.perf_counter()
    res_twenty = asyncio.run(run_twenty_concurrently())
    time_twenty = time.perf_counter() - t0

    print(
        f"\nAsync Results:\n - Single operation took: {time_single:.4f}s (Result: {res_single})"
    )
    print(
        f" - 20 concurrent operations took: {time_twenty:.4f}s (Results count: {len(res_twenty)})"
    )
    print(f" - Speedup factor: ~{20.0 / time_twenty:.1f}x theoretical limit")

    return time_single, time_twenty




@functools.lru_cache(maxsize=128)
def count_tokens(text: str) -> int:
    """Simulates a heavy token counter operation with LRU Caching."""
    time.sleep(0.05)  # Simulate CPU/IO delay
    # Simple whitespace/word proxy for tokens
    return len(text.split())


def verify_lru_cache() -> None:
    """Proves with a timer that the second call to count_tokens does zero work."""
    sample_text = "Lorem ipsum dolor sit amet, " * 1000

    # First call (Cache Miss)
    t0 = time.perf_counter()
    res1 = count_tokens(sample_text)
    dur1 = time.perf_counter() - t0

    # Second call (Cache Hit)
    t0 = time.perf_counter()
    res2 = count_tokens(sample_text)
    dur2 = time.perf_counter() - t0

    print(f"\nCache Proof:\n - 1st Call (Miss): {dur1*1000:.3f} ms (Tokens: {res1})")
    print(f" - 2nd Call (Hit):  {dur2*1000:.3f} ms (Tokens: {res2})")
    print(f" - Speedup ratio: {dur1 / max(dur2, 1e-9):.1f}x faster")


def test_cost_calculation():
    """Test 1: Verifies API cost calculation accuracy."""
    cost = calculate_cost(1000, 1000, model="gpt-4o")
    # (1000 * 0.0025 / 1000) + (1000 * 0.01 / 1000) = 0.0025 + 0.01 = 0.0125
    assert abs(cost - 0.0125) < 1e-6


def test_fence_stripper():
    """Test 2: Verifies fence stripper handles prose, fences, and non-Latin script."""
    input_text = "Some intro text...\n```json\n{\"status\": \"अमित\"}\n```\nOutro text"
    stripped = extract_json_from_fences(input_text)
    assert stripped == '{"status": "अमित"}'

    plain_text = '{"status": "ok"}'
    assert extract_json_from_fences(plain_text) == '{"status": "ok"}'


def test_phone_redactor():
    """Test 3: Verifies phone redactor replaces numbers while preserving 11+ digit IDs."""
    text = "Call 123-456-7890 or 9876543210. Ignore ID 12345678901."
    redacted = redact_phone_numbers(text)
    assert redacted == "Call [PHONE] or [PHONE]. Ignore ID 12345678901."


def test_pydantic_json_loading():
    """Test 4: Verifies Pydantic model validation with optional fields and error handling."""
    valid_json = '{"name": "Aspirin", "dose": "500mg"}'
    med = Medication.model_validate_json(valid_json)
    assert med.name == "Aspirin"
    assert med.dose == "500mg"

    # Test missing optional field
    med_no_dose = Medication.model_validate_json('{"name": "Ibuprofen"}')
    assert med_no_dose.dose is None

    # Test invalid field type
    try:
        Medication.model_validate_json('{"name": "Tylenol", "dose": 500}')
        assert False, "Should have raised ValidationError"
    except ValidationError:
        assert True




print("--- 1. Testing Generator (800-char chunks) ---")
long_string = "A" * 2000
chunks = list(chunk_text(long_string, chunk_size=800))
print(f"Generated {len(chunks)} chunks with lengths: {[len(c) for c in chunks]}")

print("\n--- 2 & 3. Async & Concurrent Operations ---")
run_async_benchmarks()

print("\n--- 4. LRU Cache Verification ---")
verify_lru_cache()
    
print("\nTo run the unit tests with pytest, run:\n       uv run pytest task_8.py")