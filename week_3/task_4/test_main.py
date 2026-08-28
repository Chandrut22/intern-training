import os

import httpx
from dotenv import load_dotenv
from langchain.chat_models import init_chat_model
from langchain.tools import tool
from langchain_core.messages import HumanMessage, SystemMessage

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


def test_university():

    response = model_with_tools.invoke(
        [
            SystemMessage(content="Use tools when appropriate."),
            HumanMessage(
                content="Find universities in Canada with McGill in the name."
            ),
        ]
    )

    assert response.tool_calls
    assert response.tool_calls[0]["name"] == "search_universities"


def test_states():

    response = model_with_tools.invoke(
        [
            SystemMessage(content="Use tools when appropriate."),
            HumanMessage(content="What are the states in India?"),
        ]
    )

    assert response.tool_calls
    assert response.tool_calls[0]["name"] == "search_country_states"


def test_calculate():

    response = model_with_tools.invoke(
        [
            SystemMessage(content="Always use calculate for mathematics."),
            HumanMessage(content="What is 2 ** 10?"),
        ]
    )

    assert response.tool_calls
    assert response.tool_calls[0]["name"] == "calculate"


def test_direct_answer():

    response = model_with_tools.invoke(
        [
            SystemMessage(content="Answer general questions directly."),
            HumanMessage(content="What is the capital of France?"),
        ]
    )

    assert not response.tool_calls
