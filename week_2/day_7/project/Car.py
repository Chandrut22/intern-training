from Vehicle import Vehicle

class Car(Vehicle):
    def __init__(self, vehicle_id, model):
        super().__init__(vehicle_id, model)
        self.rate_per_day = 50

    def calculate_rent(self, days):
        return days * self.rate_per_day