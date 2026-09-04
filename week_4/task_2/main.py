import pypdf
from langchain_core.documents import Document
from langchain_text_splitters import (
    CharacterTextSplitter,
    MarkdownHeaderTextSplitter,
    RecursiveCharacterTextSplitter,
)


def load_pdf_pages(file_path: str) -> list[Document]:
    reader = pypdf.PdfReader(file_path)
    return [
        Document(
            page_content=page.extract_text() or "",
            metadata={"source": file_path, "page": i},
        )
        for i, page in enumerate(reader.pages)
    ]


file_path = r"C:\Genworx\intern-training\week_4\task_2\document.pdf"
docs = load_pdf_pages(file_path)

fixed_splitter = CharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=200,
    separator="",
)
fixed_splits = fixed_splitter.split_documents(docs)

recursive_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=200,
    add_start_index=True,
)
recursive_splits = recursive_splitter.split_documents(docs)

combined_text = "\n\n".join([doc.page_content for doc in docs])
headers_to_split_on = [
    ("#", "Header 1"),
    ("##", "Header 2"),
    ("###", "Header 3"),
]

markdown_splitter = MarkdownHeaderTextSplitter(headers_to_split_on=headers_to_split_on)
structure_splits = markdown_splitter.split_text(combined_text)

stored_chunk_sets = {
    "fixed": fixed_splits,
    "recursive": recursive_splits,
    "structure_aware": structure_splits,
}

print(f"Fixed splits: {len(fixed_splits)}")
print(f"Recursive splits: {len(recursive_splits)}")
print(f"Structure-aware splits: {len(structure_splits)}")


def inspect_chunks(splits: list[Document], max_inspect: int = 50):
    for i, chunk in enumerate(splits[:max_inspect]):
        content = chunk.page_content.strip()
        # print(content)

        is_mid_sentence = not content.endswith((".", "!", "?", ":"))

        is_furniture = len(content) < 30 and any(char.isdigit() for char in content)

        lost_heading = not content.startswith(("#", "Item", "Section")) and i > 0

        print(
            f"Chunk {i}: Mid-sentence={is_mid_sentence}, Furniture={is_furniture}, Lost Heading={lost_heading}"
        )


print("\nInspecting recursive splits:")
inspect_chunks(recursive_splits)


print(type(recursive_splits[0]))
print(recursive_splits[0])
