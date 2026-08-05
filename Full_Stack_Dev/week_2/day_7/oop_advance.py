# Four Pillars of oop:
#   abstraction - hiding the internal details and show the essentail deatils only

#   encapsulation - blind the data attributes and function into single unit. it can be achiving by using getter and setter and access modifers

#   polymorphism - is many forms and allow the same method, function or operator to differently depends on object and args. there are two types:
#                   - Runtime polymorphism: it means the behaviour of method is decided while program is running based on object calling it
#                   - CompileTime polymorphism: it cannot be achieve 100% because it a intreprator language but it can achieve by *args and **kwargs

#   inheritance - share a one class properties and behaviour to the another class. there are five types:
#                   - Single: a child class inherit from one parent class
#                   - Multiple: a child class inherit from multiple parent class
#                   - Multilevel : a child class inherit from one parent class which in turn inherits from another parent class
#                   - Hierarchial : More than one child class inherit from a single parent class
#                   - Hybrid : a Combination of more than one type of inheritance

# Super keyword is used to access the data and call the function from the parent inside the child class

# Special methods: 

# __new__ is static method creates a new instance of class cls and takes in the class as first args.
# __init__ is a constructor is used to initialize the instance of variables
# __del__ is a destructor method which is called as soon as all reference of object is deleted
# __delete__ is used to delete the attribute of the current class
# __str__ is used to return the Custom String representation for the users
# __repr__ is used to return the Custom String representation of the developer to debugging, logging etc..



from abc import ABC, abstractmethod

class Animal(ABC):

    @abstractmethod
    def speak(self):
        pass

class Dog(Animal):

    def speak(self):
        print("Woof!!!!")

class Cat(Animal):

    def speak(self):
        print("Meow!!!!")

class Goat(Animal):

    def speak(self):
        print("Maaia!!!!")


l = [Dog() , Cat(), Goat()]

for c in l:
    c.speak()


class Shape(ABC):

    def __init__(self):
        self.pi = 3.14159

    @abstractmethod
    def area(self):
        pass

class Circle(Shape):
    def __init__(self,radius):
        super().__init__()
        self.radius = radius
    
    def area(self):
        return self.pi * (self.radius ** 2)
    
class Rectangle(Shape):
    def __init__(self, height, width):
        self.height = height
        self.width = width

    def area(self):
        return self.height * self.width
    
    def __str__(self):
        return f"The area of the rectangle is {self.height * self.width}"

c = Circle(5)
r = Rectangle(4,6)

print(c.area())
print(r.area())
print(r)
