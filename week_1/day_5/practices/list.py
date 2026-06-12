
# List append
fruits = ["apple", "banana"]
fruits.append("cherry")
print(fruits)  

# Extend
fruits = ["apple", "banana"]
tropical = ["mango", "pineapple"]
fruits.extend(tropical)
print(fruits)  
# Output: ['apple', 'banana', 'mango', 'pineapple']

# insert
fruits = ["apple", "banana", "cherry"]
fruits.insert(1, "blueberry")
print(fruits)  

fruits.insert(0, "first")
print(fruits)  


# Remove
fruits = ["apple", "banana", "apple", "cherry"]
fruits.remove("apple")  
print(fruits)  
fruits = ["apple", "banana", "cherry"]

# Pop
last_item = fruits.pop()
print(last_item)  
print(fruits)     

first_item = fruits.pop(0)
print(first_item) 
print(fruits)     

# Clear
fruits = ["apple", "banana", "cherry"]
fruits.clear()
print(fruits)  


# Index (Search)
fruits = ["apple", "banana", "cherry", "banana", "date"]
print(fruits.index("banana"))  
print(fruits.index("banana", 2))  


# Count
fruits = ["apple", "banana", "apple", "cherry", "apple"]
apple_count = fruits.count("apple")
print(apple_count)  


# Sort
fruits = ["cherry", "apple", "banana"]
fruits.sort()
print(fruits)  

# Reverse
fruits.sort(reverse=True)
print(fruits)  

fruits.sort(key=lambda item: len(item))
print(fruits)  

fruits = ["apple", "banana", "cherry"]
fruits.reverse()

print(fruits)  

# Copy
original = ["apple", "banana"]
duplicate = original.copy()

duplicate.append("cherry")

print(original)   # Output: ['apple', 'banana'] (Unchanged)
print(duplicate)  # Output: ['apple', 'banana', 'cherry']


# List Comprehension
squares = list(map(lambda x: x**2, range(10)))
print(squares)


numbers = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]

print(numbers[2:6])  

print(numbers[:4])   

print(numbers[5:])   

print(numbers[:])    

print(numbers[::2])  

print(numbers[1:8:3]) 

print(numbers[-3:])  

print(numbers[2:-2]) 

print(numbers[::-1]) 

