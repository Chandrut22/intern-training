import random

# for loop is used for iteration over a sequence of data (list, tuple, dict etc) or user know the fixed number of iteration
# continue keyword is used for skip the current iteration and proceeds to next one
# break keyword is used for terminate the loop immediatly before the loop comes to the end
# while loop used to repeat block of code until certain condition is met
# else is used on both for and while loop it can be executed only the loop is completed fully without encountor break statment
# range() functions is used to generates sequence of numbers. Syntax: range(start, end, step)
# pass statement is null statement which can be used as placeholder for future code.

# Mini program 1
n = int(input("Enter the Multiplication table: "))
for i in range(1,11):
    print(f"\n{i} X {n} = {i*n}")


# Mini program 2
count = 0
for i in range(1,101):
    count += i
print("\nSum of the number from 1 to 100 is",count)


# Mini program 3
print("\n")
for i in range(15,31):
    if(i%2 == 0 and i%3 == 0): print("FizzBuzz")
    elif(i%2 == 0): print("Fizz")
    elif(i%3 == 0): print("Buzz")
    else: print(i)


# Mini program 4
num = random.randint(0,100)
while(True):
    user = int(input("\nEnter the guessing number:"))
    if(user == num):
        print("\nCongratulations!!!\nYou found corrct number")
        break
    elif(user < num): print("\nWrong one!\nNumber is greater than given number")
    else: print("\nWrong one!\nNumber is lesser than than given number")

