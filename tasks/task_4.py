from src.token.token_accumulator import TokenAccumulator
from src.chunk import DocumentChunk
from src.summarizer import TruncateSummarizer, WordCountSummarizer
from src.role import Role


acc = TokenAccumulator()
print(f"add 500  -> running cost {acc.add(500)}")
print(f"add 1500 -> running cost {acc.add(1500)}")
print(f"total tokens: {acc.total_tokens}, report: {acc.report()}\n")

chunk = DocumentChunk(text="Hello world", page=1, source="intro.txt")
print(f"DocumentChunk: {chunk}\n")

sample = "Python supports multiple programming paradigms including OOP."
print(f"Truncate  : {TruncateSummarizer(20).summarize(sample)}")
print(f"WordCount : {WordCountSummarizer().summarize(sample)}\n")

role = Role.USER
print(f"Valid role: {role.value}")

try:
    bad = Role("usesr")  # typo
except ValueError as e:
    print(f"Misspelled role -> {e}")

