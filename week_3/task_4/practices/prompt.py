import os

from dotenv import load_dotenv
from langchain.chat_models import init_chat_model
from langchain_core.load import dumps
from langchain_core.prompts import FewShotPromptTemplate, PromptTemplate

load_dotenv()

os.environ["OPENROUTER_API_KEY"] = os.getenv("OPEN_ROUTER_KEY")

model = init_chat_model(
    model="openai/gpt-oss-20b",
    model_provider="openrouter",
    temperature=0.7,
    max_retries=6,
)

prompt_template = PromptTemplate(
    template="Explain the concept of {topic} in under {length} sentences.",
    input_variables=["topic", "length"],
)

user_topic = input("\nEnter Topic to Study: ")
user_length = input("Enter Length of Response: ")

dynamic_prompt = prompt_template.format(topic=user_topic, length=user_length)

print(f"\nQuery after filling blank fields: {dynamic_prompt}\n")

response = model.invoke(dynamic_prompt)
print(f"Response: {response.content}\n")


# -----------------------------------------------------------------------------------------------
examples = [
    {"shape": "Square", "sides": "Eight (8)"},
    {"shape": "Triangle", "sides": "Six (6)"},
]

example_prompt = PromptTemplate(
    input_variables=["shape", "sides"], template="Shape: {shape}\nSides: {sides}\n"
)

few_shot_prompt = FewShotPromptTemplate(
    examples=examples,
    example_prompt=example_prompt,
    prefix="Understand the pattern and provide me the response for my query.",
    suffix="Shape: {shape}",
    input_variables=["shape"],
)

dumps("saved_template.json")
# few_shot_prompt = load_prompt("saved_template.json")

final_prompt = few_shot_prompt.format(shape="Pentagon")

print("\nFull Prompt:\n")
print(final_prompt)

response = model.invoke(final_prompt)
print(response.content)
