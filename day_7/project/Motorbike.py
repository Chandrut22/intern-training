from Vehicle import Vehicle

class Bike(Vehicle):
    def __init__(self, vehicle_id, model):
        super().__init__(vehicle_id, model)
        self.rate_per_day = 20

    def calculate_rent(self, days):
        return days * self.rate_per_day