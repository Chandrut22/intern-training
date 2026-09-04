from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_postgres import PGVector
from langchain.chat_models import init_chat_model
from langchain_core.output_parsers import StrOutputParser
from langchain_openai import OpenAIEmbeddings
from dotenv import load_dotenv
import os
from langchain_core.prompts import ChatPromptTemplate
from operator import itemgetter
import pypdf

load_dotenv()

# Environment Setup
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

# 1. Load and Chunk Documents (Using the Winning Strategy: 2000, 200)
file_path = r"C:\Genworx\intern-training\week_4\task_4\Document.pdf"
docs = load_pdf_pages(file_path)
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=2000, chunk_overlap=200, add_start_index=True
)
all_splits = text_splitter.split_documents(docs)

# 2. Setup Embeddings and Vector Store
embeddings = OpenAIEmbeddings(
    model="openai/text-embedding-3-small",
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPEN_ROUTER_KEY"),
)

vector_store = PGVector(
    embeddings=embeddings,
    collection_name="langchain_docs_optimized",
    connection=os.getenv("DATABASE_URL"),
    use_jsonb=True,
    pre_delete_collection=True,
)

vector_store.add_documents(all_splits)
retriever = vector_store.as_retriever()

# 3. Setup LLM and RAG Chain
model = init_chat_model(
    model="openai/gpt-oss-20b",
    model_provider="openai",
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPEN_ROUTER_KEY"),
    temperature=0.7,
)

system_prompt = (
    "You are a coding assistant specialized in LangChain. "
    "Answer the user's question using the retrieved documentation as the main source of truth. "
    "If the retrieved documentation is insufficient, clearly say that you do not have enough information.\n\n"
    "Retrieved Documentation:\n{context}\n\n"
    "User Question:\n{input}"
)

prompt = ChatPromptTemplate.from_messages([
    ("system", system_prompt),
    ("human", "{input}"),
])

rag_chain = (
    {"context": itemgetter("input") | retriever | (lambda docs: "\n\n".join(d.page_content for d in docs)),
     "input": itemgetter("input")}
    | prompt
    | model
    | StrOutputParser()
)

# 4. Run a test query
if __name__ == "__main__":
    query = "What are the three major components used in the code examples of the book?"
    response = rag_chain.invoke({"input": query})
    print(f"Question: {query}\nAnswer: {response}")
