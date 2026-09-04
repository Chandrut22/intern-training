from langchain_postgres import PGVector
from langchain_openai import OpenAIEmbeddings
from app.core.settings import settings

embeddings = OpenAIEmbeddings(
    model="openai/text-embedding-3-small",
    base_url="https://openrouter.ai/api/v1",
    api_key=settings.OPENROUTER_API_KEY,
)

vector_store = PGVector(
    embeddings=embeddings,
    collection_name="langchain_docs",
    connection=settings.VECTORBASE_URL,
    use_jsonb=True,
    async_mode=True,
)

retriever = vector_store.as_retriever()