import json
import os

import httpx
from dotenv import load_dotenv
from pydantic import BaseModel, ConfigDict, Field, HttpUrl, RootModel

load_dotenv()

UNIVERSITY_BASE_URL = "http://universities.hipolabs.com"
OPENROUTER_API_KEY = os.getenv("OPEN_ROUTER_KEY")
MODEL = "openai/gpt-oss-20b"
OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"

HEADERS = {
    "Authorization": f"Bearer {OPENROUTER_API_KEY}",
    "Content-Type": "application/json",
}


class University(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    state_province: str | None = Field(default=None, alias="state-province")
    name: str
    domains: list[str]
    alpha_two_code: str
    web_pages: list[HttpUrl]
    country: str


class UniversityList(RootModel[list[University]]):
    pass


def search_universities(name: str, country: str = "") -> list[dict]:
    try:
        response = httpx.get(
            f"{UNIVERSITY_BASE_URL}/search",
            params={"name": name, "country": country},
            timeout=10.0,
        )
        response.raise_for_status()

        universities_wrapper = UniversityList.model_validate(response.json())
        universities = universities_wrapper.root

        print(f"Found {len(universities)} universities")
        for university in universities:
            print(f"\nName: {university.name}")
            print(f"Country: {university.country}")
            print(f"Code: {university.alpha_two_code}")
            print(f"State: {university.state_province}")
            print(f"Domains: {university.domains}")
            print(f"Web Pages: {[str(url) for url in university.web_pages]}")

        # Return as list of dicts for JSON serialization
        return [
            {
                "name": u.name,
                "country": u.country,
                "alpha_two_code": u.alpha_two_code,
                "state_province": u.state_province,
                "domains": u.domains,
                "web_pages": [str(url) for url in u.web_pages],
            }
            for u in universities
        ]

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


def search_country_states(name:str) -> dict:
        try:
            response = httpx.post(
                "https://countriesnow.space/api/v0.1/countries/states",
                json={"country": name},
                follow_redirects=True,
                timeout=10.0,
            )
            response.raise_for_status()
            data = response.json()

            print("Status:", response.status_code)
            print("URL:", response.url)
            print("Response:", response.text)

            if(data["error"]): return data["msg"]
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

def calculate(expression: str) -> float:
    try:
        result = eval(expression, {"__builtins__": {}}, {})
        return result
    except Exception as e:
        return f"Calculation error: {e}"

tools = [
    {
        "type": "function",
        "function": {
            "name": "search_universities",
            "description": "Search for universities by name and optional country using the Hipolabs University API.",
            "parameters": {
                "type": "object",
                "properties": {
                    "name": {
                        "type": "string",
                        "description": "Name or partial name of the university to search for."
                    },
                    "country": {
                        "type": "string",
                        "description": "Optional country name to filter results."
                    }
                },
                "required": ["name"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "search_country_states",
            "description": "Search for states by country name using the Countries Space API.",
            "parameters": {
                "type": "object",
                "properties": {
                    "name": {
                        "type": "string",
                        "description": "Name of the country to search for."
                    }
                },
                "required": ["name"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "calculate",
            "description": "Perform a mathematical calculation from a mathematical expression.",
            "parameters": {
                "type": "object",
                "properties": {
                    "expression": {
                        "type": "string",
                        "description": "Mathematical expression such as '25 * 4 + 10'."
                    }
                },
                "required": ["expression"]
            }
        }
    }
]

TOOL_MAPPING = {"search_universities": search_universities, "search_country_states":search_country_states,"calculate": calculate}


def call_llm(messages: list) -> dict:
    response = httpx.post(
        OPENROUTER_URL,
        headers=HEADERS,
        json={"model": MODEL, "tools": tools, "messages": messages},
        timeout=30.0,
    )
    response.raise_for_status()
    with open("data.json","w") as f:
        json.dump(response.json(),f,indent=4)
    msg = response.json()["choices"][0]["message"]
    messages.append(msg)
    return msg


def execute_tool(msg: dict) -> dict:
    tool_call = msg["tool_calls"][0]
    tool_name = tool_call["function"]["name"]
    tool_args = json.loads(tool_call["function"]["arguments"])

    print(f"\n[Tool Call] {tool_name}({tool_args})")
    result = TOOL_MAPPING[tool_name](**tool_args)

    return {
        "role": "tool",
        "tool_call_id": tool_call["id"],
        "content": json.dumps(result),
    }


def run_agent(user_query: str):
    messages = [
        {"role": "system", "content": "You are a helpful assistant that can search for universities."},
        {"role": "user", "content": user_query},
    ]

    max_iterations = 10
    for iteration in range(max_iterations):
    
        msg = call_llm(messages)
        # print(f"--> {msg} <-- {messages}")

        if msg.get("tool_calls"):
            tool_response = execute_tool(msg)
            messages.append(tool_response)
        else:
            print(f"\n[Assistant]: {msg['content']}")

            return msg["content"]

    print("Warning: Maximum iterations reached")
    return None


run_agent("Find universities in Canada with 'McGill' in the name.")
run_agent("what are the states in 'India' ?")
run_agent("What is (125 + 48) ** 2?")