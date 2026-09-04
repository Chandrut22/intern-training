from langchain_text_splitters import CharacterTextSplitter, MarkdownHeaderTextSplitter, RecursiveCharacterTextSplitter


text = "Chunking is an essential step in building RAG pipelines for LLMs. It ensures the model gets precise context."

# Initialize the splitter
character_splitter = CharacterTextSplitter(
    separator=" ",     # Splits at spaces to avoid cutting words in half
    chunk_size=35,     # Maximum characters per chunk
    chunk_overlap=10   # Character overlap between consecutive chunks
)

chunks = character_splitter.split_text(text)

print("Charater Splitter")

for i, chunk in enumerate(chunks):
    print(f"Chunk {i+1}: '{chunk}'")



text = """Artificial Intelligence has evolved rapidly. Today, Large Language Models handle massive datasets.

However, to make them accurate, we need Retrieval-Augmented Generation (RAG). 
RAG helps by fetching relevant data snippets before answering."""

# Initialize the splitter
recursive_splitter = RecursiveCharacterTextSplitter(
    chunk_size=100,       # Targets 100 characters per chunk
    chunk_overlap=20,     # Overlaps by 20 characters
    separators=["\n\n", "\n", " ", ""] # Order of splitting priority
)

chunks = recursive_splitter.split_text(text)

print("Recursive Splitter")

for i, chunk in enumerate(chunks):
    print(f"Chunk {i+1}:\n{chunk}")
    print("-" * 20)



markdown_document = """
# Main Topic: Machine Learning
Learning models find patterns in data.

## Subtopic: Supervised Learning
This requires labeled data to train the model.

## Subtopic: Unsupervised Learning
This finds hidden patterns in unlabeled data.
"""

# Define which markdown headers to split on and how to label them in metadata
headers_to_split_on = [
    ("#", "Header 1"),
    ("##", "Header 2"),
]

markdown_splitter = MarkdownHeaderTextSplitter(headers_to_split_on=headers_to_split_on)
chunks = markdown_splitter.split_text(markdown_document)

print("Document Splitter")

for i, chunk in enumerate(chunks):
    print(f"Chunk {i+1} Metadata: {chunk.metadata}")
    print(f"Content: {chunk.page_content.strip()}")
    print("-" * 20)
