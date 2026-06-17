class RentalAgency:
    def __init__(self):
        self.inventory = {}     # Key: vehicle_id, Value: Vehicle object
        self.__total_revenue = 0  # Private attribute (Encapsulation)

    def add_vehicle(self, vehicle):
        """Adds a new vehicle to the agency inventory."""
        if vehicle.id in self.inventory:
            print(f"\n Error: Vehicle ID {vehicle.id} already exists.")
            return False
        self.inventory[vehicle.id] = vehicle
        print(f"\n Successfully added {type(vehicle).__name__}: {vehicle.model} (ID: {vehicle.id})")
        return True

    def rent_vehicle(self, vehicle_id, days):
        """Rents out a vehicle and calculates the earnings."""
        if vehicle_id not in self.inventory:
            print("\n Error: Vehicle ID not found.")
            return

        vehicle = self.inventory[vehicle_id]
        if not vehicle.is_available:
            print("\n Error: This vehicle is already rented.")
            return

        cost = vehicle.calculate_rent(days)
        vehicle.is_available = False
        self.__total_revenue += cost  # Accessing private data safely internally
        print(f"\n Successfully rented {vehicle.model}!")
        print(f" Total Rent for {days} days: ${cost}")

    def return_vehicle(self, vehicle_id):
        """Returns a rented vehicle back to inventory."""
        if vehicle_id not in self.inventory:
            print("\n Error: Vehicle ID not found.")
            return

        vehicle = self.inventory[vehicle_id]
        if vehicle.is_available:
            print("\n This vehicle is already available in the garage.")
            return

        vehicle.is_available = True
        print(f"\n {vehicle.model} (ID: {vehicle_id}) has been returned and is available again.")

    def view_available_vehicles(self):
        """Shows all vehicles currently available for rent."""
        available = [v for v in self.inventory.values() if v.is_available]
        if not available:
            print("\n No vehicles available at the moment.")
            return

        print("\n--- Available Inventory ---")
        for v in available:
            type_name = type(v).__name__
            print(f"[{type_name}] ID: {v.id} | Model: {v.model} | Rate: ${v.rate_per_day}/day")

    def get_revenue(self):
        """Safe access to the private __total_revenue variable."""
        return self.__total_revenue