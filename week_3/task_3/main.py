import os

import httpx
from dotenv import load_dotenv
from langchain.chat_models import init_chat_model
from langchain.tools import tool
from langchain_core.messages import HumanMessage, SystemMessage, ToolMessage
from pydantic import BaseModel

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
    """Search for states by country name using the Countries Space API."""
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


class Article(BaseModel):
    title: str
    author: str
    year: int
    summary: str


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
structured_model = model.with_structured_output(Article)


def ask(prompt: str):

    messages = [SystemMessage(content="You are a helpful assistant.")]
    messages.append(HumanMessage(content=prompt))

    while True:
        response = model_with_tools.invoke(messages)
        messages.append(response)

        if not response.tool_calls:
            print(response.content)
            return

        for call in response.tool_calls:
            name, args = call["name"], call["args"]
            res = tools_name[name].invoke(args)
            res = tools_name[name].invoke(args)
            messages.append(
                ToolMessage(
                    content=str(res),
                    tool_call_id=call["id"],
                )
            )
            # print(messages)
            print(f" --> tool called {name}({args}) = {res}")


ask("Find universities in Canada with 'McGill' in the name.")
ask("what are the states in 'India' ?")
ask("What is (125 + 48) ** 2?")


prompt = """I was reading this fascinating piece the other day.
    It was written by Jane Smith back in 2021 and titled
    "The Future of Open-Weight Models". Really insightful stuff
    about how smaller models are closing the gap with proprietary ones."""

messages = [
    SystemMessage(content="Extract the article information from the user's text.")
]
messages.append(HumanMessage(content=prompt))
response = structured_model.invoke(messages)

print("\n Structured Model")
print(response)
print(type(response))

print("\nTitle:", response.title)
print("Author:", response.author)
print("Year:", response.year)
print("Summary:", response.summary)
