from dataclasses import dataclass


@dataclass(frozen=True)
class DocumentChunk:
    """A chunk of a document: text, page number, and source identifier."""

    text: str
    page: int
    source: str
