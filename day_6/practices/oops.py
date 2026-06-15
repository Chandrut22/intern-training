class Student:
    def __init__(self,name,age):
        self.name = name
        self.age = age
    
    def details(self):
        print(f"Name : {self.name}\nAge  : {self.age}")
    
stu = Student("Chan",22)
stu.details()


#--------------------------------------------------------------
class MyClass:
    """A simple example class"""
    i = 12345

    def f(self):
        return 'hello world'
    

print(MyClass.i)
print(MyClass.f)
# print(MyClass.f()) #error because we uses self as parameter so we need to create a object to call the function
x = MyClass()
print(x.f())

#--------------------------------------------------------------
class MyClass:
    """A simple example class"""
    i = 12345

    def f():
        return 'hello world'
    

print(MyClass.i)
print(MyClass.f)
print(MyClass.f()) 
print(MyClass.__doc__)

#---------------------------------------------------------------
class Complex:
    def __init__(self, realpart, imagpart):
        self.r = realpart
        self.i = imagpart

x = Complex(3.0, -4.5)
print(x.r)
print(x.i)


#---------------------------------------------------------------

class Dog:

    kind = 'canine'         # class variable shared by all instances

    def __init__(self, name):
        self.name = name    # instance variable unique to each instance

d = Dog('Fido')
e = Dog('Buddy')
print(d.kind)               
print(e.kind)              
print(d.name)              
print(e.name)               

#---------------------------------------------------------------------------
class Dog:

    tricks = []             # mistaken use of a class variable

    def __init__(self, name):
        self.name = name

    def add_trick(self, trick):
        self.tricks.append(trick)

d = Dog('Fido')
e = Dog('Buddy')
d.add_trick('roll over')
e.add_trick('play dead')
print(d.tricks)              # unexpectedly shared by all dogs

#----------------------------------------------------------------------------
class Dog:

    def __init__(self, name):
        self.name = name
        self.tricks = []    # creates a new empty list for each dog

    def add_trick(self, trick):
        self.tricks.append(trick)

d = Dog('Fido')
e = Dog('Buddy')
d.add_trick('roll over')
e.add_trick('play dead')
print(d.tricks)
print(e.tricks)


# ---------------------------------------------------------------------------------

# Access Modifiers


class Student:
    def __init__(self, name, age):
        self.name = name      
        self.age = age        
    def displayAge(self):        
        print("Age:", self.age)

obj = Student("R2J", 20)

print("Name:", obj.name)
obj.displayAge()

# -------------------------------------------------------------------------------------
class Student:
    def __init__(self, name, roll, branch):
        self._name = name            
        self._roll = roll           
        self._branch = branch       

    def _displayRollAndBranch(self): 
        print("Roll:", self._roll)
        print("Branch:", self._branch)


class School(Student):
    def displayDetails(self):
        print("Name:", self._name)  
        self._displayRollAndBranch() 


obj = School("R2J", 1706256, "IT")
obj.displayDetails()

obj1 = Student("R2J", 1706256, "IT")
print(obj1._branch, obj1._name)

#------------------------------------------------------------------------------------------------


class Student:
    def __init__(self, name, roll, branch):
        self.__name = name         
        self.__roll = roll          
        self.__branch = branch     

    def __displayDetails(self):     
        print("Name:", self.__name)
        print("Roll:", self.__roll)
        print("Branch:", self.__branch)

    def accessPrivateFunction(self):
        self.__displayDetails()    


obj = Student("R2J", 1706256, "CSE")
obj.accessPrivateFunction()
# obj.__displayDetails() # Error because this method is private
print(obj._Student__name) # name mangling

# --------------------------------------------------------------------------------------------------

class Super:
    publicData = "Public Data Member"
    _protectedData = "Protected Data Member"
    __privateData = "Private Data Member"

    def accessPrivateMembers(self):
        print("Accessing inside class:", self.__privateData)


class Sub(Super):
    def accessProtectedMembers(self):
        print("Accessing inside subclass:", self._protectedData)

obj = Sub()

print(obj.publicData)
print(obj._protectedData)
obj.accessPrivateMembers()
print(obj._Super__privateData)


# --------------------------------------------------------------------------------------------------

class Student:
    """
    Student data and Representing class
    """
    def __init__(self,name,grade):
        self.name = name
        self.grade = grade

    def __str__(self):
        return f"I am {self.name}, Studing {self.grade} Grade"
    
obj = Student("Chan",12)
print(obj)
print(obj.__str__())
print(str(obj))
print(obj.__doc__)

# ------------------------------------------------------------------------------------------

# create outer class
class Doctors:
    def __init__(self):
        self.name = 'Doctor'
        self.den = self.Dentist()
        self.car = self.Cardiologist()

    def show(self):
        print('In outer class')
        print('Name:', self.name)

    # create a 1st Inner class
    class Dentist:
        def __init__(self):
            self.name = 'Dr. Savita'
            self.degree = 'BDS'

        def display(self):
            print("Name:", self.name)
            print("Degree:", self.degree)

    # create a 2nd Inner class
    class Cardiologist:
        def __init__(self):
            self.name = 'Dr. Amit'
            self.degree = 'DM'

        def display(self):
            print("Name:", self.name)
            print("Degree:", self.degree)


# of outer class
outer = Doctors()
outer.show()

# of 1st inner class
d1 = outer.den

# of 2nd inner class
d2 = outer.car
print()
d1.display()
print()
d2.display()

# -------------------------------------------------------------------------------------
# create an outer class
class School:

    def __init__(self):
        # create an inner class object
        self.inner = self.Inner()

    def show(self):
        print('This is an outer class')

    # create a 1st inner class

    class Inner:
        def __init__(self):
            # create an inner class of inner class object
            self.innerclassofinner = self.Innerclassofinner()

        def show(self):
            print('This is the inner class')

        # create an inner class of inner

        class Innerclassofinner:
            def show(self):
                print('This is an inner class of inner class')


# create an outer class object
outer = School()
outer.show()
print()

# create an inner class object
obj1 = outer.inner
obj1.show()
print()

# create an inner class of inner class object
obj2 = outer.inner.innerclassofinner
obj2.show()