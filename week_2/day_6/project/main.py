from BookingSystem import BookingSystem

obj = BookingSystem()

for i in range(0,4):
    idno = int(input("Enter the Customer id: "))
    pickpoint = input("Enter the Pickup point: ")
    droppoint = input("Enter the Dropup point: ")
    pickuptime = int(input("Enter the Pickup Time: "))
    obj.booking(pickpoint,droppoint,pickuptime)

print(obj)
