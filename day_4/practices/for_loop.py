# range() function

for i in range(5):
    print(i)
print()

for i in range(1,5):
    print(i)
print()

for i in range(0,11,2):
    print(i)
print()

count = 0
for i in range(6,0,-1):
    count += 1
print()


# List
l = ["apple","orange","pineapple"]
for i in l:
    print(i,end=" ")
print()


# String
for i in "Chandru":
    print(i,end=" ")
print()


# tuple
t = (1,2,3,4,"Chan")
for i in t:
    print(i)
print()


# Set
s = {2,3,4,3,4,6,7,7}
for i in s:
    print(i, end=" ")
print()


# dict
d = {'q':1,'w':2,'e':3}
for i in d:
    print(i,d.get(i),end=" ")
print()


# enumerate
for i,v in enumerate(s):
    print(i,v,end=" ")
print()


# pass 
for i in range(5):
    pass
print()


# break 
for i in range(5):
    if(i == 3): break
    print(i)
print()


# continue
for i in range(5):
    if(i == 3): continue
    print(i)
print()


# else statment
for i in range(5):
    print(i)
else:
    print("After completing the loop else block is executed")
print()


for i in range(5):
    if(i == 3): continue
    print(i)
else:
    print("After completing the loop else block is executed")
print()

for i in range(5):
    if(i == 3): break
    print(i)
else:
    print("After completing the loop else block is executed")
print()


# matrix 
arr = [
    [1,2,3,4],
    [5,6,7,8],
    [9,0,10,11]
]

for i in range(len(arr)):
    for j in arr[i]:
        print(j,end=" ")
    print()


for _ in range(5):
    print(_)


# Reverse a String
s = "Chandru"
rev = ""
for c in s:
    rev = c+rev
print(rev)

# Palidrome
n = len(s)
for i in range(0,n):
    if(s[i] != s[n-1-i]):
        print("Not a palidrome")
        break
else:
    print("it's a palindrome")