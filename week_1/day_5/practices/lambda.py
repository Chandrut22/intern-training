make_multiplier = lambda multiplier: (lambda number: number * multiplier)

double = make_multiplier(2)
triple = make_multiplier(3)

print(double(5))  # Output: 10
print(triple(5))  # Output: 15


calculator = {
    "add": lambda x, y: x + y,
    "subtract": lambda x, y: x - y,
    "multiply": lambda x, y: x * y,
    "divide": lambda x, y: x / y if y != 0 else "Error"
}

print(calculator["add"](10, 5))       
print(calculator["multiply"](4, 3))  # Output: 12
print(calculator["divide"](10, 0))    # Output: Error

students = [("Alice", 90, 20), ("Bob", 90, 18), ("Charlie", 85, 22)]

sorted_students = sorted(students, key=lambda student: (-student[1], student[2]))

print(sorted_students)
# Output: [('Bob', 90, 18), ('Alice', 90, 20), ('Charlie', 85, 22)]


cleaners = [
    lambda text: text.strip(),
    lambda text: text.lower(),
    lambda text: text.replace("!", "")
]

raw_input = "  Hello WORLD!!!   "

current_text = raw_input
for cleaner in cleaners:
    current_text = cleaner(current_text)

print(current_text)  # Output: "hello world"

