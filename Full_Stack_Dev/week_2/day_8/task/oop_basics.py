# oop is a programming paradigm that organizes the software design around data (attributes) and methods (behaviour) packaged into reusable structure called class and objects
# class is defined as user designed - template or prototype. it is collection of data attributes and method.
# object is a instance of class. it hold its own set of data and methods defines by its class
# __init__() is act as a Constructor and is automatically executed when the object is created. It is used to initialize the values providied at the time of object creation.
# __str__() method allow to define the custom string representation of object.
# self is a parameter refers to the current object of the class. it used to access the attributes and methods that belongs to that object.

# Four pillars of opp:
#   - Inheritance - share the properties and behavour of class shared to another class
#   - Polymorphism - means many form that can accts on based on the users inputs
#   - Abstraction - Hiding the internal implementation and show the essentail details
#   - encapsulation - Blinding the data attributes and functions into single unit

# Types of access modifiers
#   - Public - members (methods and attributes) declared as public to access from anywhere in python
#   - Protected - members is considered protected if its name starts with single underscore(_). the members can not be accessed outside the class except by subclass
#   - Private - members is considered to private if its name starts with double underscore(__). it can be access only using self.__var in inside the class and outside the class, private data is accessing using name mangling: obj._Super__private data

# Inner class - a class defined inside a another class is called inner class or nested class
# Types of Inner class 
#   - Multiple Inner class
#   - Multilevel Inner class

class Student:
    def __init__(self,name,grade):
        self.name = name
        self.grade = grade
    
    def study(self):
        print(f"{self.name} is studing {self.grade} grade")

student1 = Student("Chandru","10")
student2 = Student("Balaji","10")

student1.study()
student2.study()

class BankAccount:
    def __init__(self,balance):
        self.__balance = balance

    def deposit(self,amt):
        self.__balance += amt
        print(f"Amount Deposit successfully\nThe Current Balance is : ${self.__balance}")

    def withdraw(self,amt):
        if(amt <= self.__balance):
            self.__balance -= amt
            print("Amount Withdrawed Successfully")
        else:
            print("Account don't have that much balance")

account1 = BankAccount(5000)
account1.withdraw(2550)
account1.deposit(6000)


account2 = BankAccount(2000)
account2.withdraw(2550)
account2.deposit(6000)
account2.withdraw(2550)

