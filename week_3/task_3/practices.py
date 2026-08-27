import os
from langchain.chat_models import init_chat_model
from langchain_openrouter import ChatOpenRouter
from dotenv import load_dotenv
from langchain.tools import tool
import httpx
import json

load_dotenv()

os.environ["OPENROUTER_API_KEY"] = os.getenv("OPEN_ROUTER_KEY")
UNIVERSITY_BASE_URL = "http://universities.hipolabs.com"


model = init_chat_model(
    "openai/gpt-oss-20b",
    model_provider="openrouter",
    temperature=0.7,
    # timeout=30,
    # max_tokens=1000,
    max_retries=6,
)

# model = ChatOpenRouter(model="openai/gpt-oss-20b",openrouter_provider="")

response = model.invoke("Why do parrots talk?")


print(response)

print("\n Streaming:")

for chunk in model.stream("Why do parrots have colorful feathers?"):
    print(chunk.text, end="", flush=True)


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


model_with_tool = model.bind_tools([search_universities])

messages = [{"role": "user", "content": "Find universities in Canada with 'McGill' in the name."}]
ai_msg = model_with_tool.invoke(messages)

messages.append(ai_msg)

# Step 2: Execute tools and collect results
for tool_call in ai_msg.tool_calls:
    tool_result = search_universities.invoke(tool_call)
    messages.append(tool_result)

response = model_with_tool.invoke(messages)

# for tool_call in response.tool_calls:
#     # View tool calls made by the model
#     print(f"Tool: {tool_call['name']}")
#     print(f"Args: {tool_call['args']}")

with open("data.json","w") as file:
    # f.writelines(response.to_json()
    json.dump(response.to_json(),file,indent=4)


print("\n",messages)






