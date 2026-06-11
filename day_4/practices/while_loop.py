# While loop
count = 0
while count < 3:
    count = count + 1
    print("Hello World")
print()

# Infinite loop
# age = 28
# while age > 19:
#     print('Infinite Loop')


# continue Statment
i = 0
a = 'chandru'
while i < len(a):
    if a[i] == 'a' or a[i] == 'd':
        i += 1
        continue
    print(a[i])
    i += 1


# Break statement
i = 0
a = 'chandru'
while i < len(a):
    if a[i] == 'a' or a[i] == 'd':
        i += 1
        break
    print(a[i])
    i += 1

# Pass statement
a = 'geeksforgeeks'
i = 0
while i < len(a):
    i += 1
    pass
print('Value of i :', i)


# else statment 
i = 0
while i < 4:
    i += 1
    print(i)
else:
    print("No Break\n")

i = 0
while i < 4:
    i += 1
    print(i)
    break
else:
    print("No Break") 

print()  

# Matrix
arr = [
    [1,2,3,4],
    [5,6,7,8],
    [9,0,10,11]
]

n = len(arr)
m = len(arr[0])
i = 0
j = 0

while(i<n):
    while(j<m):
        print(arr[i][j],end=" ")
        j+=1
    j=0
    i+=1
    print()
print()


# palindrome
s = "madam"
i = 0
j = len(s)-1
while(i < j):
    if(s[i] != s[j]):
        print("Not a palindrom")
        break
    i+=1
    j-=1
else:
    print("palindrome")


