print("\nNumber Clasifier")
num = int(input("Enter a number: "))
if(num > 0): print("It is a positive number")
elif(num < 0): print("It is a negative number")
else: print("It is a Zero")
if(num%2 == 0): print("It is a even number")
else: print("It is a odd number")


print("\nLetter Grade Calculator")
num = float(input("Enter the number from 100 - 0: "))
if(num > 100 or num < 0): print("invalid input")
elif(num >= 90): print("A")
elif(num >= 80): print("B")
elif(num >= 70): print("C")
elif(num >= 60): print("D")
elif(num >= 50): print("E")
else: print("F")

print("\nSimple Login Check Comparing\nCreate a Account")
username = str(input("Enter the username :"))
password = str(input("Enter the password :"))
retype = str(input("Re-enter the password :"))
if(retype == password): 
    print("Account created Successfully")
    print("----Login Page----")
    user = str(input("Enter the name :"))
    pas = str(input("Enter the password :"))
    if(pas == password and username == user): 
        print("Login Successfully")
    elif(pas != password):
        print("Invalid password")
    else:
        print("Invalid username")
else:
    print("Password mismatch founded\nTry again Later")


print("\nLargest of three numbers")
n1 = float(input("Enter the number 1: "))
n2 = float(input("Enter the number 2: "))
n3 = float(input("Enter the number 3: "))
if(n1==n2 and n2==n3): print("All Three number are equal")
elif(n1 > n2 and n1 > n3): print(f"{n1} is a largest number")
elif(n2 > n1 and n2 > n3): print(f"{n2} is a largest number")
else: print(f"{n3} is a largest number")