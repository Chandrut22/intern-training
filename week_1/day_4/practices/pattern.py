
n = int(input("Enter the number of lines of pyramid"))

# Half Pyramid

for i in range(0,n):
    for j in range(0,i+1):
        print("*",end=" ")
    print("\n")

for i in range(0,n):
    for j in range(0,i+1):
        print(str(j+1),end=" ")
    print("\n")


# Inverted Half Pyramid

for i in range(0,n):
    for j in range(0,n-i):
        print("*",end=" ")
    print("\n")

for i in range(0,n):
    for j in range(0,n-i):
        print(j+1,end=" ")
    print("\n")


# Full pyramid

for i in range(n):
    for j in range(n-1-i):
        print(" ",end = " ")
    
    for k in range(i+1):
        print(k+1,end=" ")

    for l in range(i):
        print(l+1,end=" ")
    
    print("\n")


