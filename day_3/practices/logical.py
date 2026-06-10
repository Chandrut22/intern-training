print("\nLOGICAL AND OPERATOR (and)")
print(True and True)
print(True and False)
print(5 > 3 and 10 > 2)
print(4 == 4 and 1 > 10)
age = 25
has_id = True
print(age >= 18 and has_id)
username = "admin"
password = "123"
print(username == "admin" and password == "123")
score = 85
print(score > 80 and score <= 100)
print(bool("text") and bool(5))
print(bool([]) and bool("hello"))
print((2 + 2 == 4) and (5 * 2 == 10))

print("\nLOGICAL OR OPERATOR (or)")
print(True or False)
print(False or False)
print(5 > 10 or 2 > 1)
print(3 == 4 or 7 < 2)
is_weekend = True
is_holiday = False
print(is_weekend or is_holiday)
role = "Guest"
print(role == "Admin" or role == "Guest")
temperature = 35
print(temperature < 0 or temperature > 30)
print(bool("") or bool("Python"))
print(bool(0) or bool([]))
print((10 / 2 == 5) or (1 == 0))

print("\nLOGICAL NOT OPERATOR (not)")
print(not True)
print(not False)
print(not (5 > 3))
print(not (10 == 20))
is_logged_in = False
print(not is_logged_in)
has_errors = True
print(not has_errors)
print(not "text")
print(not "")
print(not (4 < 2 and 5 > 1))
print(not (10 > 5 or 1 > 2))


print("\nCOMBINATION OF LOGICAL OPERATORS")
print((True and False) or not False)
print(not True or (True and not False))

age = 20
has_ticket = True
is_vip = False
print((age >= 18 and has_ticket) or not is_vip)

score = 75
has_extra_credit = False
is_passing = True
print((score > 80 or has_extra_credit) and not is_passing)

username = "user1"
is_admin = False
is_moderator = True
print((username == "admin" or is_moderator) and not is_admin)

temperature = 15
is_raining = True
is_sunny = False
print((temperature > 20 and is_sunny) or not is_raining)

balance = 50
has_credit = True
is_frozen = False
print((balance > 100 or has_credit) and not is_frozen)

item_count = 5
coupon_valid = False
free_shipping = True
print((item_count >= 10 and coupon_valid) or not free_shipping)

is_weekend = True
has_homework = True
parent_approved = False
print((is_weekend and not has_homework) or parent_approved)

x = 10
y = 20
z = 30
print((x < y and not y > z) or x == z)
