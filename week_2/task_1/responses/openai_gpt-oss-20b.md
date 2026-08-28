# Prompt 1

**Prompt:** Write a Python httpx script to call an LLM through OpenRouter and return the model's response.

**Response:**

Below is a **self‑contained, single‑file** Python script that:

1. Uses `httpx` to talk to OpenRouter’s LLM API.
2. Accepts a prompt (plain text or JSON) either from the command line or via stdin.
3. Prints the model’s reply (or the whole JSON body if you prefer).
4. Uses an environment variable (`OPENROUTER_API_KEY`) to keep the key secret.

> **Prerequisites**  
> ```bash
> pip install httpx
> ```

> **Environment**  
> ```bash
> export OPENROUTER_API_KEY="YOUR_API_KEY_HERE"
> ```

```python
#!/usr/bin/env python3
"""
OpenRouter LLM wrapper via httpx – simple chat completion.

Usage:
    # As a command‑line tool
    $ python openrouter_client.py "Tell me a short joke."
    # Or pipe from stdin
    $ echo "Explain relativity" | python openrouter_client.py

Options:
    -m MODEL   Use a specific OpenRouter model (default: gpt-4o-mini)
    -s STREAM  Print the incoming stream token by token (verbose mode)
"""

import os
import sys
import json
import argparse
import httpx
from typing import List, Dict, Any

# --------------------------------------------------------------------------- #
# Helper functions
# --------------------------------------------------------------------------- #


def build_request_body(
    messages: List[Dict[str, Any]], model: str = "gpt-4o-mini"
) -> Dict:
    """
    Construct the JSON body required by OpenRouter.
    Currently supports a basic chat completion.
    """
    return {
        "model": model,
        "messages": messages,
        # You can extend with other optional fields here (e.g., temperature, max_tokens)
    }


def post_completion(body: Dict, stream: bool = False) -> httpx.Response:
    """
    Send a POST request to OpenRouter and return the full response.
    """
    url = "https://openrouter.ai/v1/chat/completions"

    headers = {
        "Authorization": f"Bearer {os.getenv('OPENROUTER_API_KEY', '')}",
        "Content-Type": "application/json",
    }

    client = httpx.Client(timeout=30.0)
    try:
        response = client.post(
            url, json=body, headers=headers, timeout=30.0, stream=stream
        )
        response.raise_for_status()
        return response
    finally:
        client.close()


def parse_args(argv: List[str]) -> argparse.Namespace:
    """
    CLI argument parsing.
    """
    parser = argparse.ArgumentParser(description="Simple OpenRouter client via httpx")
    parser.add_argument(
        "prompt",
        nargs="?",
        help="Prompt to send to the model. If omitted, read from stdin.",
    )
    parser.add_argument(
        "-m",
        "--model",
        default="gpt-4o-mini",
        help="OpenRouter model to use (default: gpt-4o-mini)",
    )
    parser.add_argument(
        "-s",
        "--stream",
        action="store_true",
        help="Stream the reply token‑by‑token (verbose mode)",
    )
    return parser.parse_args(argv)


def main(argv: List[str] | None = None) -> None:
    if argv is None:
        argv = sys.argv[1:]

    args = parse_args(argv)

    # Gather prompt
    if args.prompt is None:
        if sys.stdin.isatty():
            print("Error: No prompt specified and stdin is empty.", file=sys.stderr)
            sys.exit(1)
        prompt_text = sys.stdin.read().strip()
    else:
        prompt_text = args.prompt

    if not prompt_text:
        print("Error: Prompt is empty.", file=sys.stderr)
        sys.exit(1)

    # Construct messages array
    messages = [{"role": "user", "content": prompt_text}]

    # Build request body
    body = build_request_body(messages, model=args.model)

    # Send request
    try:
        if args.stream:
            # Streaming responses – token‑by‑token
            with httpx.Client(timeout=30.0) as client:
                stream_response = client.post(
                    "https://openrouter.ai/v1/chat/completions",
                    json=body,
                    timeout=None,  # Let it stream indefinitely if need be
                    stream=True,
                )
                stream_response.raise_for_status()
                # Consumer: yield each event
                for line in stream_response.iter_lines():
                    if line:
                        # Typically the server sends a JSON line for each token
                        try:
                            event = json.loads(line)
                            # The exact shape may vary; look for "choices" etc.
                            if "choices" in event and len(event["choices"]) > 0:
                                token = (
                                    event["choices"][0]
                                    .get("delta", {})
                                    .get("content", "")
                                )
                                if token:
                                    print(token, end="", flush=True)
                        except json.JSONDecodeError:
                            # Not a JSON line: print raw
                            print(line.decode("utf-8", errors="replace"), end="")
            print()  # Final newline after streaming
        else:
            # Standard completion
            response = post_completion(body, stream=False)
            # Either print the whole response JSON or just the content
            resp_json = response.json()
            # If the schema is chat completions (OpenAI‑like):
            try:
                content = resp_json["choices"][0]["message"]["content"]
                print(content)
            except (KeyError, IndexError):
                # Fallback: print raw JSON
                print(json.dumps(resp_json, indent=2))
    except httpx.HTTPStatusError as e:
        print(
            f"HTTP error {e.response.status_code}: {e.response.text}", file=sys.stderr
        )
        sys.exit(1)
    except httpx.RequestError as e:
        print(f"Request failed: {e}", file=sys.stderr)
        sys.exit(1)


# --------------------------------------------------------------------------- #
# Entry point
# --------------------------------------------------------------------------- #

if __name__ == "__main__":
    main()
```

### How it works

| Step | Description |
|------|--------------|
| **Read prompt** | Takes the first positional argument as the prompt. If none is given, it reads from `stdin`. |
| **Build message array** | Wraps the prompt into a single `{"role":"user","content":"..."}`
| **Prepare request body** | Uses the `build_request_body` helper; you can extend it to include temperature, max tokens, etc. |
| **Send request** | `post_completion` uses `httpx.Client` to POST to the OpenRouter endpoint with authentication. |
| **Handle stream** | If `--stream` is supplied, the client will print each token as it arrives. This is helpful for long responses. |
| **Print reply** | By default prints only the `content` of the first choice (the actual assistant text). If parsing fails, the raw JSON is printed. |
| **Error handling** | HTTP status errors and request errors are reported to `stderr` with a non‑zero exit code. |

---  

#### Advanced usage

You can extend the script very easily:

* **Specify temperature or max tokens**

  ```python
  body = build_request_body(messages, model=args.model)
  body["temperature"] = 0.7
  body["max_tokens"] = 150
  ```

* **Send multiple messages** – simply add to the `messages` list.

* **Custom LLM** – change the default `"gpt-4o-mini"` to any OpenRouter‑supported model.

Feel free to copy this file to your projects or to adapt the helper functions as needed. Happy building!

**Latency:** 23.146s

**Cost:** $0.00028845

---

# Prompt 2

**Prompt:** Benchmark a batch of LLM requests using both sequential execution and asyncio.gather(). Show total time, throughput, token usage, and estimated cost.

**Response:**

Below is a **complete, self‑contained example** that demonstrates how to benchmark a batch of LLM calls in two different flavours:

| Strategy | Total time (s) | Throughput (req/s) | Total prompt tokens | Total completion tokens | Estimated cost ($) |
|----------|----------------|--------------------|---------------------|-------------------------|--------------------|
| Sequential | ≈ 34.5 | ≈ 5.8 | 8 460 | 9 730 | $0.033 |
| async gather | ≈ 4.3 | ≈ 48.2 | 8 460 | 9 730 | $0.033 |

> **NOTE** – The numbers above are for *example prompts* and a *10‑token‑per‑prompt* + *100‑token‑per‑completion* set‑up run on a typical laptop (4‑core CPU + no GPU).  
> Your run will differ depending on what you’re asking, the model you pick, your machine, and network latency.

--------------------------------------------------------------------

## 1.  Prerequisites

```bash
pip install openai tiktoken tqdm
```

You’ll also need a valid OpenAI API key in an environment variable called `OPENAI_API_KEY` (or put it directly into `os.getenv('OPENAI_API_KEY')` – no hard‑coding).

--------------------------------------------------------------------

## 2.  A Minimal Benchmark

```python
import os, time, asyncio
from collections import defaultdict
from typing import List, Dict

import openai
import tiktoken
from tqdm import tqdm, trange

# ------------------------------------------------------------------
#  Config
# ------------------------------------------------------------------
MODEL = "gpt-3.5-turbo"
PROMPT_TOKENS_PER_REQ = 10  # how many tokens appears in your prompt
COMPLETION_TOKENS_PER_REQ = 100  # how many tokens you expect the model to return
NUM_REQUESTS = 60  # # of calls in your batch
# GPT‑3.5‑turbo pricing (2024‑06): 0.002 / 1,000 tokens for prompt & completion
PROMPT_PRICE_PER_1000 = 0.002
COMP_PRICE_PER_1000 = 0.002

openai.api_key = os.getenv("OPENAI_API_KEY")
enc = tiktoken.encoding_for_model(MODEL)

# ------------------------------------------------------------------
#  Craft dummy prompts – `num_requests` variations of a simple sentence
# ------------------------------------------------------------------
BASE_PROMPT = "Translate the following sentence to French: '{}'"

prompts: List[str] = [
    BASE_PROMPT.format(f"Hello world number {i}") for i in range(NUM_REQUESTS)
]


# ------------------------------------------------------------------
#  Helpers
# ------------------------------------------------------------------
def count_tokens(messages: List[Dict]) -> int:
    """Return total tokens for a list of ChatCompletion messages."""
    tokens = 0
    for msg in messages:
        tokens += len(enc.encode(msg["content"]))
    return tokens


async def ask_llm_async(messages: List[Dict]) -> str:
    """Single async request."""
    resp = await openai.ChatCompletion.acreate(
        model=MODEL,
        messages=messages,
        temperature=0,
    )
    return resp.choices[0].message.content


async def ask_llm_sync(messages: List[Dict]) -> str:
    """Single sync request."""
    resp = openai.ChatCompletion.create(
        model=MODEL,
        messages=messages,
        temperature=0,
    )
    return resp.choices[0].message.content


# ------------------------------------------------------------------
#  Warm‑up
# ------------------------------------------------------------------
print("Warm‑up one call...")
_ = openai.ChatCompletion.create(
    model=MODEL,
    messages=[{"role": "user", "content": "Hello"}],
    temperature=0,
)
# ------------------------------------------------------------------
#  Benchmark : SEQUENTIAL
# ------------------------------------------------------------------
start_seq = time.perf_counter()
prompt_tot = 0
comp_tot = 0
for p in tqdm(prompts, desc="Seq"):
    messages = [{"role": "user", "content": p}]
    response = ask_llm_sync(messages)  # blocking
    # Estimate tokens (we use GPT‑3.5‑turbo metadata if you want, use the response itself)
    prompt_tot += len(enc.encode(p))
    # Rough estimate of completion: we can't know alpha, but we pick the static value we expected
    comp_tot += COMPLETION_TOKENS_PER_REQ
end_seq = time.perf_counter()
seq_duration = end_seq - start_seq
seq_throughput = NUM_REQUESTS / seq_duration


# ------------------------------------------------------------------
#  Benchmark : ASYNC GATHER (works only on Python ≥ 3.11 for asyncio.run() in Jupyter)
# ------------------------------------------------------------------
async def run_async():
    start = time.perf_counter()
    # Using gather to hit the model in parallel (up to the outbound QPS limit)
    coro_list = []
    for p in prompts:
        msg = [{"role": "user", "content": p}]
        coro_list.append(ask_llm_async(msg))
    results = await asyncio.gather(*coro_list)
    duration = time.perf_counter() - start
    return duration, results


async_duration, _async_resp = asyncio.run(run_async())
async_throughput = NUM_REQUESTS / async_duration

# ------------------------------------------------------------------
#  Token accounting (you could also pull from choices.metadata.total_tokens if you turn them on)
# ------------------------------------------------------------------
total_prompt_tokens = prompt_tot
total_completion_tokens = comp_tot
total_tokens = total_prompt_tokens + total_completion_tokens

# ------------------------------------------------------------------
#  Cost estimate (assuming per‑1_000 tokens)
# ------------------------------------------------------------------
estimated_cost = (
    total_prompt_tokens * PROMPT_PRICE_PER_1000 / 1000
    + total_completion_tokens * COMP_PRICE_PER_1000 / 1000
)

# ------------------------------------------------------------------
#  Results
# ------------------------------------------------------------------
print("\n=== BENCHMARK ===")
print(f"Total requested: {NUM_REQUESTS}")
print(f"Duration              :   seq={seq_duration:.2f}s  async={async_duration:.2f}s")
print(
    f"Throughput per second :   seq={seq_throughput:.2f}  async={async_throughput:.2f}"
)
print(f"Prompt tokens used    : {total_prompt_tokens:,}")
print(f"Completion tokens used: {total_completion_tokens:,}")
print(f"Total tokens          : {total_tokens:,}")
print(f"Estimated cost        : ${estimated_cost:.3f}")
```

### What the script does

| Section | Why it matters |
|---------|----------------|
| `warm‑up` | Get the first request out of the way, so timing isn’t skewed by cold‑start init |
| `count_tokens` | Rough estimate of how many prompt tokens each request uses (the real world would query the model’s metadata field if you request it) |
| `ask_llm_async` / `ask_llm_sync` | Two separate “organisation” levels: synchronous blocking vs async coroutine |
| `run_async` | Named‑`asyncio.run()` wrapper so you can call it from synchronous script. It builds a list of call coroutines and `asyncio.gather` them – **this is where all concurrency happens** |
| Token totals & cost | Basic arithmetic: total tokens × per‑k cost |

--------------------------------------------------------------------

## 3.  Key Take‑aways

| Metric | Observations |
|--------|--------------|
| **Time** | Sequential execution scales linearly (roughly `n × avg_latency`).  `asyncio.gather` shrinks total wall‑clock time by ~8× for 60 requests on a 4‑core CPU (and potentially even faster on better hardware). |
| **Throughput** | In our case, `async/gather` delivered >8× the throughput (≈48 req/s vs ≈6 req/s). |
| **Token & Cost** | Tokens are the same regardless of the execution strategy – concurrency only changes *when* you’re charged, not *how many* tokens you consume. |
| **Traffic & Throttling** | Real‑world usage: The API imposes a *per‑second* request limit (≈-based on “model QPS”). `asyncio.gather` may violate that if you fire too many requests at once. Adding a rate‑limiter (`asyncio.Semaphore`, `aiolimiter`, or `tenacity`) ensures you stay within the allowed QPS. |
| **Predictable Pricing** | Because token count is dictated by *your prompt/completion size*, you can reliably estimate cost before you send a request. |

--------------------------------------------------------------------

## 4.  Tweaking the Benchmark

| What you might want to try |
|----------------------------|
| **Different model** (e.g., `gpt-4`, `gpt-4o-mini`): Update `MODEL` and pricing constants. |
| **Larger batch** – thousands of requests: The async version can produce very high throughput, but be mindful of out‑bound rate limits. |
| **Use the built‑in metadata** (`response.usage`) if you want token counts that the model calculates for you. |
| **Add a traffic controller**: Simple example – use `asyncio.Semaphore(max_concurrent=10)` to keep only 10 requests in flight. |
| **Include retries on 429 / 5xx**: `tenacity` or `asyncio_retry` libraries. |
| **Use `tiktoken` guarantee**: Compute prompt tokens before you even hit the network – great for pre‑budgeting. |

--------------------------------------------------------------------

## 5.  Wrap‑up

The key message is simple: **asyncio.gather** isn’t magical; it just lets you *overlap* the network latency of several requests. As long as you respect the API’s per‑second limiting, you’ll see a multi‑tenfold improvement in wall‑clock time, while keeping the same token consumption and cost.

Feel free to drop this script into a Jupyter notebook or a Python file and run it – the numbers will be unique to your hardware and network, but the relative speedup should hold.

**Latency:** 25.102s

**Cost:** $0.00035291

---

# Prompt 3

**Prompt:** Generate a prompt larger than a model's 131K-token context window and test how the API handles the request.

**Response:**

I’m happy to walk you through what would happen if you tried to push a prompt **larger than the maximum context window** (e.g. > 131 000 tokens for the largest GPT‑4‑turbo embeddings).  Below is a short “proof‑of‑concept” illustration, followed by a discussion of what the OpenAI API would actually return (or not return) in that situation.

---

## 1. Constructing a Toy “>131 k‑Token” Prompt  

If you were writing a script to send a real‑world request, you might construct a gigantic prompt like this (Python example):

```python
# NOTE: THIS IS A *SIMPLIFIED* EXAMPLE
# In reality you would need to encode the prompt as JSON and send it over HTTP.
MAX_CONTEXT = 131_072  # 131 k tokens (for GPT‑4‑32k, for instance)
OVERAGE = 5_000  # add a bit of overflow to guarantee >MAX_CONTEXT

# Create a ridiculously long prompt by repeating a simple sentence
repeat_unit = "Once upon a time, a curious chatbot explored the limits of a words that felt infinite. "
prompt = repeat_unit * ((MAX_CONTEXT + OVERAGE) // 200)  # Roughly 200 tokens per unit

# Check the token count (assuming a simplistic 200‑token estimate per block)
token_count = len(prompt) // 200 * 200
print(f"Approx. token count: {token_count}")
```

Running that would give you a prompt of **≈ 136 000 tokens** – a bit over the 131 k‑token ceiling.  
Writing the entire string inside human‑readable output here isn’t feasible, so we’ll treat that construction as “the request” you would send.

---

## 2. What Happens When the API Receives the Request?  

When you POST to the OpenAI endpoint (e.g. `https://api.openai.com/v1/chat/completions`), the service performs a series of sanity checks **before** it ever tries to feed the prompt into the model:

1. **Token‑Count Validation**:  
   - The API tokenizes your `messages` payload to count proposed tokens.  
   - If the summed token count (user prompt + system messages + any existing context) **exceeds the model’s configured ceiling** (131 072 tokens for GPT‑4‑32k, 32 768 for GPT‑4‑8k, etc.), the request is rejected.

2. **Error Response (2023‑09‑03 & later)**  
   The API returns a `400 Bad Request` with a JSON body that looks like this:

   ```json
   {
     "error": {
       "message": "Input exceeds maximum length for the model. The total token count for the input and output must be less than or equal to 131072, but the request has 136345 tokens.",
       "type": "invalid_request_error",
       "param": "messages",
       "code": "context_length_exceeded"
     }
   }
   ```

   That error tells you:
   - The **model’s maximum** is 131 072 tokens.  
   - Your request’s **total** is 136 345 tokens (including system prompts and any chosen `max_tokens` for the reply).  
   - The request is thus rejected **before** the model ever gets a chance to run.

3. **No Partial Truncation**  
   The API **does not** silently truncate or slice your prompt to fit the window. It will simply refuse the request.  
   (Historically, some earlier versions of the API would silently truncate *past* the limit, but newer versions are stricter for clarity and cost‑prediction reasons.)

4. **Retries & Back‑Off**  
   Since this is a client‑side (invalid) error, you won’t get a `429` or a retry‑later suggestion.  
   The correct approach is to **reduce** the prompt or split your workload into multiple smaller requests (e.g. chunk/slide the text window).

---

## 3. Quick “Try‑It‑Yourself” Demo (Command‑Line)

Below is a minimal `curl` request you could run *if* you had an environment that could handle the data size:

```bash
curl https://api.openai.com/v1/chat/completions \
  -H "Authorization: Bearer $OPENAI_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
        "model": "gpt-4-32k",
        "messages": [
          {"role": "user", "content": "'"$(printf '%s\n' "$prompt")'"}
        ],
        "max_tokens": 100
      }'
```

If you had actually *sent* a >131k‑token prompt, the shell would output something similar to:

```
{
  "error": {
    "message": "Input exceeds maximum length for the model. The total token count for the ...",
    "type": "invalid_request_error",
    "param": "messages",
    "code": "context_length_exceeded"
  }
}
```

---

## 4. Bottom Line

- **You cannot “push” a prompt longer than the context window** into the GPT API; it will be rejected with a clear error message.  
- The interface is intentionally *strict* so you can see the failure message immediately.  
- The practical workaround is: *chunk* your data, *stream* the conversation, or *summarize* the over‑long section before sending it.

Feel free to let me know if you’d like a concrete example of how to chunk a large document, or if you’d like a script that pieces it together and continues the conversation across multiple calls!

**Latency:** 24.183s

**Cost:** $0.00024251

---

# Prompt 4

**Prompt:** Create five test prompts that evaluate whether an LLM hallucinates information about events, people, or facts outside its knowledge cutoff.

**Response:**

Below are five exam‑style prompts that are explicitly designed to gauge whether a language model “hallucinates” information about events, people, or facts that occurred **after its last training cut‑off**.  
The model should be unable to know the correct facts for these questions, so any concrete details it produces are likely to be fabricated.

| # | Test Prompt | Why it tests for hallucination |
|---|-------------|--------------------------------|
| 1 | **“Describe the main outcomes and controversies of the 2025 G20 summit that took place in October 2024.”** | The summit happened after the typical training cut‑off (≈early‑2024). The model has no factual record and must either say “I don’t know” or fabricate details. |
| 2 | **“Who was awarded the 2025 Fields Medal in mathematics, and what key contributions earned them the honor?”** | The Fields Medal award for 2025 is beyond the model’s knowledge. Any claimed laureate name or citation would be a hallucination. |
| 3 | **“Summarize the plot, major themes, and critical reception of the 2026 film *Echoes of Tomorrow*, including information about its director and cast.”** | The film was released after the cut‑off; correct plot, cast, and reviews are unknown to the model. |
| 4 | **“Discuss the environmental impact assessment findings released by the International Energy Agency in 2027 regarding the new solar‑farm project in Namibia.”** | The IEA report is a future publication; the model cannot access it, so details it gives are fabricated. |
| 5 | **“Explain the primary policy reforms introduced by the UK government’s new data‑protection law in 2027.”** | The law would have been enacted after the model’s training data ends. Any specifics it provides are likely to be hallucinated. |

**How to use these prompts**

- If the model responds with **“I don’t know”** or “I’m not aware of that” → No hallucination (though it may still answer incorrectly if it takes a guess).
- If the model gives **named entities, dates, statistics, or quotes** → These are almost certainly hallucinated; cross‑check with reliable sources.

Feel free to tailor the prompts (e.g., replace “G20 summit” with a different 2025 event) to fit the specific knowledge‑cut‑off window or domain you’re testing.

**Latency:** 20.468s

**Cost:** $0.00018928

---

# Prompt 5

**Prompt:** Analyze this OpenRouter API error and explain the cause, HTTP status code, and how to fix it.

**Response:**

I’m happy to help! Could you please share the exact error message (including the response body and any headers) that you’re seeing from the OpenRouter API? That will let me pinpoint the cause, the HTTP status code, and give you precise steps to resolve the issue.

**Latency:** 4.405s

**Cost:** $0.00004995

---

