d = {}

def add_contact(name,number):
    try:
        d[name] = int(number)
        print("Contact is added successfully")

    except ValueError as e:
        print("Give the correct number ",e)

def find_contact(name):
    print("Find a Contact by "+name)
    try:
        print(f"{name} : {d[name]}")
    except KeyError as e:
        print("Name is not found",e)

def list_contacts():
    print("List a all Contacts")
    for n in d.keys():
        print(f"{n} : {d[n]}")