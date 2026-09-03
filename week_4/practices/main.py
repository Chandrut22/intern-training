import requests
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter, Language
from langchain_postgres import PGVector
from langchain.chat_models import init_chat_model
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from dotenv import load_dotenv
import os
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_core.prompts import ChatPromptTemplate


load_dotenv()

os.environ["OPENROUTER_API_KEY"] = os.getenv("OPEN_ROUTER_KEY")

DOCS_BASE = "https://docs.langchain.com"

DOC_PATHS = [
    "oss/python/langchain/agents",
    "oss/python/deepagents/rag",
    "oss/python/langchain/tools",
    "oss/python/langchain/models",
    "oss/python/deepagents/retrieval",
    "oss/python/langchain/knowledge-base",
    "oss/python/langchain/middleware",
    # "oss/python/deepagents/overview",
    "oss/python/deepagents/subagents",
    "oss/python/deepagents/streaming",
    "oss/python/deepagents/backends",
    "oss/python/langgraph/overview",
    "oss/python/langgraph/quickstart",
]


def load_langchain_docs():
    i = 0
    paths = DOC_PATHS
    docs: list[Document] = []
    for path in paths:
        url = f"{DOCS_BASE}/{path}.md"
        try:
            response = requests.get(url, timeout=20)
            response.raise_for_status()
        except requests.RequestException:
            continue
        source = f"{DOCS_BASE}/{path}"
        docs.append(
            Document(page_content=response.text, metadata={"source": source,"id":i})
        )
        i+=1
    return docs


docs = load_langchain_docs()
print(f"Loaded {len(docs)} documentation pages.")


total_chars = sum(len(doc.page_content) for doc in docs)
print(f"Total characters: {total_chars}")
print(docs[0].page_content[:500])


text_splitter = RecursiveCharacterTextSplitter.from_language(chunk_size=1000, chunk_overlap=200, language=Language.PYTHON)
all_splits = text_splitter.split_documents(docs)
print(f"Split documentation into {len(all_splits)} chunks.")

embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")


vector_store = PGVector(
    embeddings=embeddings,
    collection_name="langchain_docs",
    connection=os.getenv("DATABASE_URL"),
    use_jsonb=True,
    pre_delete_collection=True
)


vector_store.add_documents(all_splits,ids=[f"{doc.metadata['id']}_{i}" for i, doc in enumerate(all_splits)])
retriever = vector_store.as_retriever()

model = init_chat_model(
    model="openai/gpt-oss-20b",
    model_provider="openrouter",
    temperature=0.7,
    max_retries=6,
)

system_prompt = (
    "You are an assistant for question-answering tasks. "
    "Use the following pieces of retrieved context to answer "
    "the question. If you don't know, say that you don't know.\n\n"
    "{context}"
)

prompt = ChatPromptTemplate.from_messages([
    ("system", system_prompt),
    ("human", "{input}"),
])

print("Model Initialized")

def format_docs(docs):
    print(len(docs))
    print(docs)

    return "\n\n".join(doc.page_content if hasattr(doc, "page_content") else str(doc) for doc in docs)


rag_chain = (
    {
        "context": (lambda x: x["input"]) | retriever | format_docs, 
        "input": RunnablePassthrough()
    } | prompt | model | StrOutputParser())

response = rag_chain.invoke({"input": "give the sample code RAG using langchain LCEL?"})
print(response)

print("-"*60)

response = rag_chain.invoke({"input": "difference between the pandas and polars"})
print(response)

