while True:
    try:
        x = int(input("Please enter a number: "))
        break
    except ValueError:
        print("Oops!  That was no valid number.  Try again...")
# ----------------------------------------------------------------------------------------------------------------

class B(Exception):
    pass

class C(B):
    pass

class D(C):
    pass

for cls in [B, C, D]:
    try:
        raise cls()
    except D:
        print("D")
    except C:
        print("C")
    except B:
        print("B")
# --------------------------------------------------------------------------------------------------------------------

try:
    f = open('practices//myfile.txt')
    s = f.readline()
    i = int(s.strip())
except OSError as err:
    print("OS error:", err)
except ValueError:
    print("Could not convert data to an integer.")
except Exception as err:
    print(f"Unexpected {err=}, {type(err)=}")
    raise
# --------------------------------------------------------------------------------------------------------------------

def this_fails():
    x = 1/0

try:
    this_fails()
except ZeroDivisionError as err:
    print('Handling run-time error:', err)

# ------------------------------------------------------------------------------------------------------------------
# try:
#     raise NameError('HiThere')
# except NameError:
#     print('An exception flew by!')
#     raise

# -----------------------------------------------------------------------------------------------------------------

def divide(x, y):
    try:
        result = x / y
    except ZeroDivisionError:
        print("division by zero!")
    except TypeError as err:
        print("TypeError: ",err)
    else:
        print("result is", result)
    finally:
        print("executing finally clause")

divide(2, 1)


divide(2, 0)


divide("2", "1") 

# ---------------------------------------------------------------------------------

class NegativeNuumberFound(Exception):
    def __init__(self,num):
        self.num = f"Age must be greater than or equal 18, but your age is {num}"
        super().__init__(self.num)

def age_restrication(age):
    if age < 18 : raise NegativeNuumberFound(age)
    else: print("Account Created SuccessFully")

try:
    age_restrication(9)
except NegativeNuumberFound as e:
    print("Less age is founded ",e)