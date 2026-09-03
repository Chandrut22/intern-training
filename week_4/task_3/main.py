import pypdf
from langchain_core.documents import Document
from langchain_postgres import PGVector
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from dotenv import load_dotenv
import os

load_dotenv()


embeddings = GoogleGenerativeAIEmbeddings(model="models/gemini-embedding-001")

vector_store = PGVector(
    embeddings=embeddings,
    collection_name="my_docs",
    connection=os.getenv("DATABASE_URL")
)

def load_pdf_pages(file_path: str) -> list[Document]:
    reader = pypdf.PdfReader(file_path)
    return [
        Document(
            page_content=(page.extract_text() or "").replace("\x00", ""),
            metadata={"source": file_path, "page": i, "id": str(i)},
        )
        for i, page in enumerate(reader.pages)
    ]

file_path = r"C:\Genworx\intern-training\week_4\task_2\document.pdf"
docs = load_pdf_pages(file_path)


recursive_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=200,
    add_start_index=True,
)
recursive_splits = recursive_splitter.split_documents(docs)

print(len(recursive_splits))

print("Document is loaded successfully")

# print(docs[0])


vector_store.add_documents(
    recursive_splits, 
    ids=[f"{doc.metadata['id']}_{i}" for i, doc in enumerate(recursive_splits)]
)

# results = vector_store.similarity_search(
#     "Open weight ?", k=10, filter={"id": {"$in": [1, 5, 2, 9]}}
# )

results = vector_store.similarity_search(
    "what is Open weight ?", k=10
)
for doc in results:
    print(f"* {doc.page_content} [{doc.metadata}]")