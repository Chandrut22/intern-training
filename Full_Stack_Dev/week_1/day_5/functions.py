# Function is reusable block of code that executes a specific task only when it called
# Types of args: 
#   1. default args : assign a default value if caller is omits that args
#   2. keyword args : passing a args using parameter name, ignoring the position order
#   3. Arbitary args: allow the function to be accept an variable number of values at runtime
# lambda expression - small anonymous function that can be define in single line of code.
# Documentation String - is special string literal placed on very first statement inside function 
# Function annotation - is enables to add additional explanatory metadata about the args declared in function definition and  also return type

# List is a ordered, mutable collection used to store a multiple data items in single variable
# Build in function: append(), extend(), insert(), remove(), pop(), clear(), index(), count(), sort(), reverse()
# can access by index position and slicing
# List comprehension is a shorter, cleaner way to create a new list out existing list or iterable in python

# Tuple is a ordered, immutable collection used to store a mutliple data items in single variable
# Build in function: count(), index()
# can access by index position and slicing

# Set is unordered, mutable collection used to store a single data items in single varibles
# Build in function: add(), remove(), discard(), pop()
# and have a mathematical operation like union, intersection, difference, symmetric_difference

# dict is store a data in key - value pair, ordered, mutable, unique key
# Build in function: .get() .pop() .popitem() .clear()


d = {}

def add_contact(name,number):
    d[name] = number
    print("Contact is added successfully")

def find_contact(name):
    print("Find a Contact by "+name)
    for n in d.keys():
        if(name in n):
            print(f"{n} : {d[n]}")

def list_contacts():
    print("List a all Contacts")
    for n in d.keys():
        print(f"{n} : {d[n]}")

print("\nContact Book: ")

while(True):
    n = int(input("\n1. Add the contact\n2. Find the contact\n3. List the contact\n4. Exit\nEnter your Choice: "))
    if(n == 1):
        name = input("Enter the Name : ")
        number = input("Enter the number : ")
        add_contact(name,number)
    
    elif(n == 2):
        name = input("Enter the Name : ")
        find_contact(name)
    
    elif(n == 3):
        list_contacts()
    
    elif(n == 4):
        break

l = [] 

def add_task(task):
    l.append(task)
    print("Task added successfully")

def show_task():
    if(l == []): print("List is empty")
    for i in range(len(l)):
        print(f"{i+1} {l[i]}")

def remove_task(i):
    if(i <= 0 and i > len(l)):
        print("Invalid Input")
    else:
        l.pop(i)
        print("Task removed successfully")

print("\nTo-Do List")

while(True):
    n = int(input("\n1. Add the Task\n2. Remove the Task\n3. Show the Task\n4. Exit\nEnter the Choice:"))
    if(n == 1):
        task = input("Enter the Task :")
        add_task(task)
    elif(n == 2):
        show_task()
        n = int(input("Enter the task number to remove :"))
        remove_task(n-1)
    elif(n == 3):
        show_task()
    elif(n == 4):
        break
