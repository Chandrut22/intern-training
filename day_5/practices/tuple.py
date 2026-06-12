fruits = ("apple", "banana", "cherry")
print(fruits)  

one_fruit = ("apple",)  # Correct
not_a_tuple = ("apple") # Wrong 


# fruits[0] = "blueberry" -> Throws TypeError
# fruits.append("cherry") -> Throws AttributeError (no append method exists)

numbers = (0, 10, 20, 30, 40, 50)

print(numbers[1])    # Output: 10
print(numbers[-1])   # Output: 50

print(numbers[1:4])  # Output: (10, 20, 30)
print(numbers[::-1]) # Output: (50, 40, 30, 20, 10, 0)

letters = ('a', 'b', 'a', 'c', 'a')

# 1. count() - Counts occurrences
print(letters.count('a'))  # Output: 3

# 2. index() - Finds the first position of a value
print(letters.index('b'))  # Output: 1

coordinates = 40.7128, -74.0060 
print(coordinates)

lat, lon = coordinates
print(lat)  # Output: 40.7128
print(lon)  # Output: -74.0060

