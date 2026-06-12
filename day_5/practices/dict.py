user = {
    "name": "Alex",
    "age": 28,
    "is_admin": True,
    "skills": ["Python", "SQL"]
}
print(user)


# 1. Using square brackets
print(user["name"])  # Output: Alex
# print(user["email"]) -> Crashes with a KeyError

# 2. Using the .get() method (Safe: returns None or a default value if key is missing)
print(user.get("email"))         # Output: None
print(user.get("email", "N/A"))  # Output: N/A



# Add a new key-value pair
user["email"] = "alex@email.com"

# Update an existing value
user["age"] = 29

# Remove an item and get its value using .pop()
removed_value = user.pop("age") 

# Remove the last inserted item using .popitem()
last_item = user.popitem()  # Returns ('email', 'alex@email.com')

# Clear the entire dictionary
user.clear()  # Output: {}


car = {"brand": "Ford", "model": "Mustang", "year": 1964}

# 1. Loop through keys only
for key in car.keys():
    print(key)

# 2. Loop through values only
for value in car.values():
    print(value)

# 3. Loop through both (key-value pairs) using .items()
for key, value in car.items():
    print(f"{key}: {value}")


dict1 = {"a": 1, "b": 2}
dict2 = {"b": 99, "c": 4} # Note that 'b' overlaps

# Method 1: Using .update() (modifies dict1 in place)
dict1.update(dict2) 
print(dict1)

dict1 = {"a": 1, "b": 2}
dict2 = {"b": 99, "c": 4} # Note that 'b' overlaps
# Method 2: Using the merge operator (creates a new dictionary)
combined = dict1 | dict2  
print(combined)  # Output: {'a': 1, 'b': 99, 'c': 4} (overlapping keys get overwritten)

