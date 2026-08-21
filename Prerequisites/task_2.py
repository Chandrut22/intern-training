messages = [
    {
        "role": "System",
        "content": "You are a helpful assistant.",
        "tokens": 6,
    },
    {
        "role": "user",
        "content": "Hello!",
        "tokens": 2,
    },
    {
        "role": "assistant",
        "content": "Hi! How can I help you today?",
        "tokens": 8,
    },
    {
        "role": "user",
        "content": "Explain what Python dictionaries are.",
        "tokens": 7,
    },
    {
        "role": "assistant",
        "content": "A dictionary stores key-value pairs.",
        "tokens": 6,
    },
    {
        "role": "user",
        "content": "Give me an example.",
        "tokens": 5,
    },
    {
        "role": "assistant",
        "content": "Example: {'name': 'Alice', 'age': 25}",
        "tokens": 8,
    },
    {
        "role": "user",
        "content": "How do I iterate over it?",
        "tokens": 7,
    },
    {
        "role": "assistant",
        "content": "Use a for loop with the items() method.",
        "tokens": 9,
    },
    {
        "role": "user",
        "content": "Thanks!",
        "tokens": 2,
    },
]

for i, msg in enumerate(messages, start=1):
    print(
        f"{i}) User: {msg['role']}\nContent: {msg['content']}\nNo. of Token: {msg['tokens']}\nCost: {(msg['tokens'] * 0.25):.6f}\n"
    )
    msg["cost"] = msg["tokens"] * 0.25


assistant_messages_loop = []
for message in messages:
    if message["role"] == "assistant":
        assistant_messages_loop.append(message)

assistant_messages_comp = [
    message for message in messages if message["role"] == "assistant"
]

print("Results are identical:", assistant_messages_loop == assistant_messages_comp)

token_sort = sorted(messages, key=lambda x: x["tokens"])
print(token_sort)

token_counts = []

with open("C:\\Genworx\\intern-training\\prerequisites\\tokens.txt", mode="r") as f:
    for i, token in enumerate(f, start=1):
        try:
            v = int(token.strip())
            token_counts.append(v)
        except ValueError:
            print(f"Line{i}: '{token.strip()}' is not a valid integer.")

print(f"Valid Integer: {token_counts}")

decimal_total = 0
float_total = 0

for i, msg in enumerate(messages):
    decimal_total += int(msg["cost"])
    float_total += int(msg["cost"])

print(decimal_total == float_total)

text = "வணக்கம் உலகம்"

char_count = len(text)

utf8_byte_count = len(text.encode("utf-8"))

print(f"Text              : {text}")
print(f"Characters        : {char_count}")
print(f"UTF-8 byte length : {utf8_byte_count}")

print(
    "LLM tokenization is based on tokens, not characters or bytes. "
    "Texts that require more UTF-8 bytes (such as many non-Latin scripts) "
    "may also use more tokens, which can increase your token bill."
)

list1 = [10, 20, 30]
list2 = list1

list2.append(40)

print("list1:", list1)
print("list2:", list2)

print("Same object?", list1 is list2)

print(
    "Both variables reference the same list object, so a change made through one variable is visible through the other."
)
