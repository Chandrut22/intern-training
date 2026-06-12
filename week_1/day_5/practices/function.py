# function is a reusable block of code that executes a specific task only when it calles

print("\n Function printing")
def fib(n):    
    """Print a Fibonacci series less than n."""
    a, b = 0, 1
    while a < n:
        print(a, end=' ')
        a, b = b, a+b
    print()

fib(2000)
print(fib)
f = fib
f(50) 
f(0)
print(f(0))


#----------------------------------------------------------------------------------------------
print("\nFunction Returning")
def fib2(n):  
    """Return a list containing the Fibonacci series up to n."""
    result = []
    a, b = 0, 1
    while a < n:
        result.append(a)   
        a, b = b, a+b
    return result

print(fib2(100))

#----------------------------------------------------------------------------------------------

print("\nDefault Args")
# 1) Default Arguments: assign a default vaule if caller is omits that args
def power(base, exponent=2):
    return base ** exponent

print(power(4))     # Uses default exponent 2 -> 16
print(power(4, 3))  # Overrides default exponent -> 64

# 1.1) Default values are evaluted at the point of function definition in the defining scope
i = 5
def f(arg=i):
    print(arg)

i = 6
f()

# 1.2) Important warning: The default value is evaluated only once
def f(a, L=[]):
    L.append(a)
    return L

print(f(1))
print(f(2))
print(f(3))

#---------------------------------------------------------------------------------------------------------

print("\nKeyword args")
# 2) Keyword arguments: passing a arguments using parameter name, ignoring the position order
def profile(name, age):
    print(f"{name} is {age} years old.")

profile(age=25, name="Bob")

#---------------------------------------------------------------------------------------------------------

print("\nArbitary args")
# 3) Arbitary arguments: used when we do not know before hand how many args will be passed
def shipping_order(destination, *items, **delivery_notes):
    print(f"Shipping to: {destination}")
    print(f"Items: {items}")
    print(f"Notes: {delivery_notes}")

shipping_order("New York", "Laptop", "Mouse", "Keyboard", speed="Express", leave_at_door=True)

def standard_arg(arg): # it allow both position and keyword argument
    print(arg)

def pos_only_arg(arg, /): # it allow only the position
    print(arg)

def kwd_only_arg(*, arg): # it allow only the keyword
    print(arg)

def combined_example(pos_only, /, standard, *, kwd_only): # it's 2 positional and 1 keyword
    print(pos_only, standard, kwd_only)

standard_arg(2) # it print 2
standard_arg(arg=2) # it print 2

pos_only_arg(1) 
# pos_only_arg(arg=1) # Error

# kwd_only_arg(3) # Error
kwd_only_arg(arg=3)

# combined_example(1, 2, 3) # Error because it take 2 postional but it give 3 postional
combined_example(1, 2, kwd_only=3)


combined_example(1, standard=2, kwd_only=3)

#----------------------------------------------------------------------------------------------------------

print("\nLamda Expression")
# lambda Expression - is a small anonymous one - linear function in python
def make_incrementor(n):
    return lambda x: x + n

f = make_incrementor(42)
print(f(0))
print(f(1))

#----------------------------------------------------------------------------------------------------------

print("\nDocumentation String")
# Documentation String
def my_function():
    """Do nothing, but document it.

    No, really, it doesn't do anything:

        >>> my_function()
        >>>
    """
    pass

print(my_function.__doc__)

# ----------------------------------------------------------------------------------------------------------

print("Function Annotation")
# Function annotations
def f(ham: str, eggs: str = 'eggs') -> str:
    print("Annotations:", f.__annotations__)
    print("Arguments:", ham, eggs)
    return ham + ' and ' + eggs

f('spam')
