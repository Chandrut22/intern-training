from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_postgres import PGVector
from langchain.chat_models import init_chat_model
from langchain_core.output_parsers import StrOutputParser
from langchain_openai import OpenAIEmbeddings
from dotenv import load_dotenv
import os
from langchain_core.prompts import ChatPromptTemplate
import pypdf

load_dotenv()

os.environ["OPENROUTER_API_KEY"] = os.getenv("OPEN_ROUTER_KEY")


def load_pdf_pages(file_path: str) -> list[Document]:
    reader = pypdf.PdfReader(file_path)
    return [
        Document(
            page_content=page.extract_text() or "",
            metadata={"source": file_path, "page": i, "id": i + 1},
        )
        for i, page in enumerate(reader.pages)
    ]


file_path = r"C:\Genworx\intern-training\week_4\practices\Document.pdf"

docs = load_pdf_pages(file_path)

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000, chunk_overlap=200, add_start_index=True
)

all_splits = text_splitter.split_documents(docs)

print(f"Documents: {len(docs)}")
print(f"Chunks: {len(all_splits)}")

for i, chunk in enumerate(all_splits[:5]):
    print(f"\n--- Chunk {i + 1} ---")
    print(chunk.page_content)
    print(chunk.metadata)

embeddings = OpenAIEmbeddings(
    model="openai/text-embedding-3-small",
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPEN_ROUTER_KEY"),
)

vector_store = PGVector(
    embeddings=embeddings,
    collection_name="langchain_docs",
    connection=os.getenv("DATABASE_URL"),
    use_jsonb=True,
    pre_delete_collection=True,
)

vector_store.add_documents(
    all_splits, ids=[f"{doc.metadata['id']}_{i}" for i, doc in enumerate(all_splits)]
)


def search_documentation(query: str) -> str:
    retrieved_docs = vector_store.similarity_search(query, k=4)
    return retrieved_docs


retriever = vector_store.as_retriever()

model = init_chat_model(
    model="openai/gpt-oss-20b",
    model_provider="openai",
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPEN_ROUTER_KEY"),
    temperature=0.7,
    max_retries=6,
)

system_prompt = (
    "You are a coding assistant specialized in LangChain, Deep Agents, and LangGraph. "
    "Answer the user's question using the retrieved documentation as the main source of truth. "
    "When generating code, use the APIs, classes, functions, parameters, and examples provided in the documentation. "
    "Do not invent APIs, parameters, or unsupported behavior. "
    "Prefer the documented approach when writing code. "
    "If the retrieved documentation is insufficient, clearly say that you do not have enough information instead of guessing. "
    "Provide clear and practical code that directly solves the user's request.\n\n"
    "Retrieved Documentation:\n"
    "{context}\n\n"
    "User Question:\n"
    "{input}"
)

prompt = ChatPromptTemplate.from_messages(
    [
        ("system", system_prompt),
        ("human", "{input}"),
    ]
)

print("Model Initialized")


def format_docs(docs):
    print(type(docs))
    for i, doc in enumerate(docs):
        print(f"\n--- Document {i + 1} ---")
        print(f"ID: {doc.id}")
        print(f"Metadata: {doc.metadata}")
        print(f"Content:\n{doc.page_content}")
    return "\n\n".join(
        doc.page_content if hasattr(doc, "page_content") else str(doc) for doc in docs
    )


from operator import itemgetter

rag_chain = (
    {
        "context": itemgetter("input") | retriever | format_docs,
        "input": itemgetter("input"),
    }
    | prompt
    | model
    | StrOutputParser()
)

response = rag_chain.invoke({"input": "give the code RAG using langchain LCEL"})
print(response)

print("-" * 60)

response = rag_chain.invoke({"input": "give the TODO List code in react"})
print(response)
