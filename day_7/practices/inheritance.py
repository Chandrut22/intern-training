# Single Inhertance
class Parent:
	def func1(self):
		print("Parent")
	
class Child(Parent):
	def func2(self):
		print("Child")
		
obj = Child()
obj.func1()
obj.func2()


# ------------------------------------------------------------------------
# Multiple Inheritance
class Father:
    def __init__(self, name):
        self.father_name = name

class Mother:
    def __init__(self, name):
        self.mother_name = name

class Child(Father, Mother):
    def __init__(self, father, mother, child):
        Father.__init__(self, father)
        Mother.__init__(self, mother)
        self.child_name = child

obj = Child("Ramesh", "Sita", "Rahul")

print(obj.father_name)
print(obj.mother_name)
print(obj.child_name)

# ------------------------------------------------------------------------

#using super() with **kwargs
class Father:
    def __init__(self, father_name, **kwargs):
        super().__init__(**kwargs)
        self.father_name = father_name


class Mother:
    def __init__(self, mother_name, **kwargs):
        super().__init__(**kwargs)
        self.mother_name = mother_name


class Child(Father, Mother):
    def __init__(self, father_name, mother_name, child_name):
        super().__init__(
            father_name=father_name,
            mother_name=mother_name
        )
        self.child_name = child_name


obj = Child("Ramesh", "Sita", "Rahul")

print(obj.father_name)
print(obj.mother_name)
print(obj.child_name)

# -------------------------------------------------------------------------------------
# Multilevel Inheritance
class GrandFather:
    def __init__(self, name):
        self.grandfather_name = name


class Father(GrandFather):
    def __init__(self, grandfather, name):
        super().__init__(grandfather)
        self.father_name = name


class Son(Father):
    def __init__(self, grandfather, father, name):
        super().__init__(grandfather, father)
        self.son_name = name


obj = Son("Raman", "Ramesh", "Rahul")

print(obj.grandfather_name)
print(obj.father_name)
print(obj.son_name)

# ----------------------------------------------------------------------------------------
# Hierarchical Inheritance
# Base class
class Parent:
    def func1(self):
        print("This function is in parent class.")

# Derived class 1
class Child1(Parent):
    def func2(self):
        print("This function is in child 1.")

# Derived class 2
class Child2(Parent):
    def func3(self):
        print("This function is in child 2.")

# Driver code
object1 = Child1()
object2 = Child2()

object1.func1()
object1.func2()
object2.func1()
object2.func3()


#-------------------------------------------------------------------------------------------
# Hybrid Inheritance
# Base class
class School:
    def func1(self):
        print("This function is in school.")

# Derived class 1 (Single Inheritance)
class Student1(School):
    def func2(self):
        print("This function is in student 1.")

# Derived class 2 (Another Single Inheritance)
class Student2(School):
    def func3(self):
        print("This function is in student 2.")

# Derived class 3 (Multiple Inheritance)
class Student3(Student1, School):
    def func4(self):
        print("This function is in student 3.")

# Driver code
obj = Student3()
obj.func1()
obj.func2()

