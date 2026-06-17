from Rent_Agency import RentalAgency
from Car import Car
from Motorbike import Bike

agency = RentalAgency()

agency.add_vehicle(Car("C01", "Tesla Model 3"))
agency.add_vehicle(Car("C02", "Toyota Camry"))
agency.add_vehicle(Bike("B01", "Harley Davidson"))
agency.add_vehicle(Bike("B02", "Yamaha R1"))

while True:
    print(" WELCOME TO VEHICLE RENTAL OOPS")
    print("1. Login as Customer")
    print("2. Login as Admin")
    print("3. Exit Program")
        
    role_choice = input("Enter choice (1-3): ").strip()

    if role_choice == "1":
        while True:
            print("\n--- CUSTOMER MENU ---")
            print("1. View Available Vehicles")
            print("2. Rent a Vehicle")
            print("3. Return a Vehicle")
            print("4. Back to Main Menu")
                
            cust_choice = input("Select an option: ").strip()

            if cust_choice == "1":
                    agency.view_available_vehicles()
            elif cust_choice == "2":
                    agency.view_available_vehicles()
                    v_id = input("Enter Vehicle ID to rent: ").strip()
                
                    days = int(input("Enter rental duration (days): "))
                    if days <= 0:
                        print("\n Invalid days entered. Rental cancelled.")
                        break
                    agency.rent_vehicle(v_id, days)
                        
            elif cust_choice == "3":
                    v_id = input("Enter Vehicle ID to return: ").strip()
                    agency.return_vehicle(v_id)
            elif cust_choice == "4":
                    break
            else:
                    print("\n Invalid choice.")

    elif role_choice == "2":
            while True:
                print("\n--- ADMIN MENU ---")
                print("1. View Total Financial Revenue")
                print("2. Add New Vehicle to Fleet")
                print("3. Back to Main Menu")
                
                admin_choice = input("Select an option: ").strip()

                if admin_choice == "1":
                    # Accessing via public getter method
                    print(f"\n Total Agency Revenue Collected: ${agency.get_revenue()}")
                elif admin_choice == "2":
                    v_type = input("Enter type (car/bike): ").strip().lower()
                    v_id = input("Enter unique Vehicle ID: ").strip()
                    v_model = input("Enter vehicle Model: ").strip()

                    if v_type == "car":
                        agency.add_vehicle(Car(v_id, v_model))
                    elif v_type == "bike":
                        agency.add_vehicle(Bike(v_id, v_model))
                    else:
                        print("\Invalid type. Please choose 'car' or 'bike'.")
                elif admin_choice == "3":
                    break
                else:
                    print("\Invalid choice.")

    elif role_choice == "3":
            print("\nThank you for using the Vehicle Rental System. Goodbye! 👋")
            break
    else:
            print("\Choice out of bounds. Try again.")