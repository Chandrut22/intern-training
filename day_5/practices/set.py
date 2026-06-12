numbers = {1, 2, 2, 3, 4, 4, 4}
print(numbers)  # Output: {1, 2, 3, 4}

fruits = {"apple", "banana"}

# 1. add() - Adds a single element
fruits.add("cherry")
print(fruits)  # Output: {'banana', 'cherry', 'apple'} (order may vary)

# 2. remove() - Deletes an element (Crashes if item doesn't exist)
fruits.remove("banana")

# 3. discard() - Deletes an element safely (Does NOT crash if item is missing)
fruits.discard("watermelon") 

# 4. pop() - Removes and returns a random element
random_fruit = fruits.pop()

set_a = {1, 2, 3, 4}
set_b = {3, 4, 5, 6}

# Union (All unique items from both sets)
print(set_a.union(set_b))         # Output: {1, 2, 3, 4, 5, 6}
print(set_a | set_b)              # Shortcut operator

# Intersection (Items present in BOTH sets)
print(set_a.intersection(set_b))  # Output: {3, 4}
print(set_a & set_b)              # Shortcut operator

# Difference (Items in A that are NOT in B)
print(set_a.difference(set_b))    # Output: {1, 2}
print(set_a - set_b)              # Shortcut operator

# Symmetric Difference (Items in A or B, but NOT both)
print(set_a.symmetric_difference(set_b)) # Output: {1, 2, 5, 6}
print(set_a ^ set_b)                     # Shortcut operator

small = {1, 2}
large = {1, 2, 3, 4}

# Check if 'small' is inside 'large'
print(small.issubset(large))    # Output: True

# Check if 'large' contains 'small'
print(large.issuperset(small))  # Output: True

