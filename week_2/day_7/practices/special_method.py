class Student():
    def __init__(self,name):
        self.name = name


s = Student("Chan")
print(s.name)
# ------------------------------------------------------------------------------------------------------------------

class Test:
    def __init__(self):
        print("Object created")

    def __del__(self):
        print("Object destroyed")

obj = Test()
del obj
# ------------------------------------------------------------------------------------------------------------------

class MyDescriptor:

    def __delete__(self, instance):
        print("Attribute deleted")

class Employee:
    name = MyDescriptor()

e = Employee()
del e.name

# ----------------------------------------------------------------------------------------------------------------

class Student:
    def __init__(self, name):
        self.name = name

    def __str__(self):
        return f"Student Name: {self.name}"

s = Student("Chandru")
print(s)

# -----------------------------------------------------------------------------------------------------------------

class Student:
    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return f"Student('{self.name}')"

s = Student("Chandru")

print(repr(s))
