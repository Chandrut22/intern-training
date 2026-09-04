
from app.rag.vector_store import retriever
from app.rag.utils import format_docs
from app.rag.prompt import system_prompt
from app.core.settings import settings
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.chat_models import init_chat_model
from langchain_core.output_parsers import StrOutputParser
from operator import itemgetter
from langchain_core.messages import trim_messages
from langchain_core.messages.utils import count_tokens_approximately

model = init_chat_model(
    model="openai/gpt-oss-20b",
    model_provider="openrouter",
    api_key=settings.OPENROUTER_API_KEY,
    temperature=0.7,
    max_retries=6,
)

trimmer = trim_messages(
    max_tokens=3000,
    strategy="last",
    token_counter=count_tokens_approximately,
    include_system=False,
    start_on="human",
)

prompt = ChatPromptTemplate.from_messages(
    [
        ("system", system_prompt),
        MessagesPlaceholder("chat_history"),
        ("human", "{input}"),
    ]
)

rag_chain = (
    {
        "context": itemgetter("input") | retriever | format_docs,
        "input": itemgetter("input"),
        "chat_history": itemgetter("chat_history") | trimmer,
    }
    | prompt
    | model
    | StrOutputParser()
)


async def run_rag_chain(input_text: str, chat_history: list) -> str:
    return await rag_chain.ainvoke(
        {"input": input_text, "chat_history": chat_history}
    )


async def stream_rag_chain(input_text: str, chat_history: list):
    async for chunk in rag_chain.astream(
        {"input": input_text, "chat_history": chat_history}
    ):
        yield chunk