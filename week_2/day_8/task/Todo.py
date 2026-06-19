l = [] 

def add_task(task):
    l.append(task)
    print("Task added successfully")

def show_task():
    if(l == []): print("List is empty")
    for i in range(len(l)):
        print(f"{i+1} {l[i]}")

def remove_task(i):
    if(i <= 0 and i > len(l)):
        print("Invalid Input")
    else:
        l.pop(i)
        print("Task removed successfully")