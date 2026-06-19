# module is containing the python code including functions, classes and variables saved with .py extension

# module - single python file 
# package - a folder containing multiple modules and an __init__.py
# libary - a broader collection of multiple related packages 

# Ways of importing modules
#       - standard import - import contact
#       - specific import - from contact import add_contact , from contact import *
#       - Alias import - from fibo import fibo as fibonacci

# exception handling  - handling the unexcepted event that occurs during program execution.
# Build-in Exception - ImportError, IndexError, KeyError, KeyboardInterrupt, NameError, OSError, SyntaxError, IndentationError, IndentationError, ValueError, ZeroDivisionError
# Order of excution - Try -> except -> else -> finally
# raise statement allows the programmer to force specific exception is occurs




from week_2.day_8.task.Contact import add_contact, find_contact,list_contacts
from week_2.day_8.task.Todo import add_task, remove_task, show_task
import week_2.day_8.task.oop_advance as oop_advance
import week_2.day_8.task.oop_basics as oop_basics


print("\n Contact Book")

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

