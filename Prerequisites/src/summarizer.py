from abc import ABC, abstractmethod

class BaseSummarizer(ABC):
    """Base class: every subclass must implement summarize()."""

    @abstractmethod
    def summarize(self, text: str) -> str:
        """Return a summary of `text`. Subclasses must override."""
        raise NotImplementedError("Subclasses must implement summarize()")


class TruncateSummarizer(BaseSummarizer):
    """Take the first N characters."""
    def __init__(self, limit: int = 50) -> None:
        self.limit = limit

    def summarize(self, text: str) -> str:
        return text[: self.limit]


class WordCountSummarizer(BaseSummarizer):
    """Report length as 'N words'."""
    def summarize(self, text: str) -> str:
        n = len(text.split())
        return f"{n} words"