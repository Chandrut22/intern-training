class BankAccount:
    def __init__(self):
        self.balance = 1000

    def _show_balance(self):
        print(f"Balance: ₹{self.balance}")  # Protected method

    def __update_balance(self, amount):
        self.balance += amount             # Private method

    def deposit(self, amount):
        if amount > 0:
            self.__update_balance(amount)  # Accessing private method internally
            self._show_balance()           # Accessing protected method
        else:
            print("Invalid deposit amount!")
            
account = BankAccount()
account._show_balance()      # Works, but should be treated as internal
# account.__update_balance(500)  # Error: private method
account.deposit(500)         # Uses both methods internally


class Employee:
    def __init__(self):
        self.__salary = 50000  # Private attribute

    def get_salary(self):    # Getter method
        return self.__salary

    def set_salary(self, amount):   # Setter method
        if amount > 0:
            self.__salary = amount
        else:
            print("Invalid salary amount!")

emp = Employee()
print(emp.get_salary())  
emp.set_salary(60000)   
print(emp.get_salary())