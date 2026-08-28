import json
import os
from pathlib import Path

import httpx
from dotenv import load_dotenv
from langchain.chat_models import init_chat_model
from langchain.tools import tool
from langchain_core.messages import HumanMessage, SystemMessage, ToolMessage

UNIVERSITY_BASE_URL = "http://universities.hipolabs.com"


@tool
def search_universities(name: str, country: str = ""):
    """Search for universities by name and optional country using the Hipolabs University API."""

    try:
        response = httpx.get(
            f"{UNIVERSITY_BASE_URL}/search",
            params={"name": name, "country": country},
            timeout=10.0,
        )
        response.raise_for_status()

        return response.json()

    except httpx.TimeoutException:
        print("University API request timed out.")
        return []
    except httpx.HTTPStatusError as e:
        print(f"University API returned HTTP error: {e.response.status_code}")
        return []
    except httpx.RequestError as e:
        print(f"University API request failed: {e}")
        return []
    except Exception as e:
        print(f"Unexpected error: {e}")
        return []


@tool
def calculate(expression: str) -> float:
    """Perform a mathematical calculation from a mathematical expression."""
    try:
        result = eval(expression, {"__builtins__": {}}, {})
        return result
    except Exception as e:
        return f"Calculation error: {e}"


@tool
def search_country_states(name: str) -> dict:
    """Search for states, provinces, or administrative regions of a country using the Countries Now API."""
    try:
        response = httpx.post(
            "https://countriesnow.space/api/v0.1/countries/states",
            json={"country": name},
            follow_redirects=True,
            timeout=10.0,
        )
        response.raise_for_status()
        data = response.json()

        if data["error"]:
            return data["msg"]
        return data["data"]

    except httpx.TimeoutException:
        print("API request timed out.")
        return []
    except httpx.HTTPStatusError as e:
        print(f"API returned HTTP error: {e.response.status_code}")
        return []
    except httpx.RequestError as e:
        print(f"API request failed: {e}")
        return []
    except Exception as e:
        print(f"error: {e}")
        return []


tools = [search_universities, search_country_states, calculate]
tools_name = {t.name: t for t in tools}

load_dotenv()

os.environ["OPENROUTER_API_KEY"] = os.getenv("OPEN_ROUTER_KEY")

model = init_chat_model(
    model="openai/gpt-oss-20b",
    model_provider="openrouter",
    temperature=0.7,
    # timeout=30,
    # max_tokens=1000,
    max_retries=6,
)


model_with_tools = model.bind_tools(tools)


with open(Path("test.json"), "r", encoding="utf-8") as f:
    test_cases = json.load(f)


def run_test_case(test_case):
    messages = [
        SystemMessage(
            content=(
                "You are a helpful assistant. "
                "Use search_universities for university searches. "
                "Use search_country_states for states, provinces, or regions of a country. "
                "Always use calculate for mathematical calculations. "
            )
        )
    ]

    messages.append(HumanMessage(content=(test_case["prompt"])))

    tool_calls = []
    try:
        while True:
            response = model_with_tools.invoke(messages)
            messages.append(response)
            if not response.tool_calls:
                break
            for call in response.tool_calls:
                tool_calls.append({"name": call["name"], "args": call["args"]})
                result = tools_name[call["name"]].invoke(call["args"])
                messages.append(
                    ToolMessage(content=str(result), tool_call_id=call["id"])
                )
        return evaluate_result(test_case, tool_calls, response)
    except Exception as e:
        return {
            "passed": False,
            "reason": f"Execution error: {e}",
            "tool_calls": tool_calls,
        }


def evaluate_result(test_case, tool_calls, response):
    behavior = test_case["expected_behavior"]
    if behavior in ["refusal", "direct_answer"]:
        passed = len(tool_calls) == 0
        return {
            "passed": passed,
            "reason": "No tool was called" if passed else "Unexpected tool call",
            "tool_calls": tool_calls,
        }
    expected_tools = test_case.get("expected_tools", [])
    actual_tools = [call["name"] for call in tool_calls]
    if actual_tools != expected_tools:
        return {
            "passed": False,
            "reason": f"Expected tools {expected_tools}, got {actual_tools}",
            "tool_calls": tool_calls,
        }
    expected_args = test_case.get("expected_args")
    if expected_args and tool_calls:
        for key, expected_value in expected_args.items():
            actual_value = tool_calls[0]["args"].get(key)
            if actual_value != expected_value:
                return {
                    "passed": False,
                    "reason": f"Argument '{key}': expected {expected_value!r}, got {actual_value!r}",
                    "tool_calls": tool_calls,
                }
    return {
        "passed": True,
        "reason": "Expected tool and arguments matched",
        "tool_calls": tool_calls,
    }


def run_eval():
    passed = 0
    failed = 0
    for test_case in test_cases:
        result = run_test_case(test_case)
        if result["passed"]:
            passed += 1
            print(f"\n[PASS] Test {test_case['id']}: {test_case['prompt']}")
        else:
            failed += 1
            print(
                f"\n[FAIL] Test {test_case['id']}: {test_case['prompt']} - {result['reason']}"
            )
        print(result)
    total = len(test_cases)
    pass_rate = passed / total * 100 if total else 0
    print(
        f"\nTotal: {total} | Passed: {passed} | Failed: {failed} | Pass Rate: {pass_rate:.2f}%"
    )


if __name__ == "__main__":
    run_eval()
