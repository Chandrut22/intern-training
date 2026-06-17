from abc import ABC, abstractmethod

class Vehicle(ABC):
    def __init__(self, vehicle_id, model):
        self.id = vehicle_id
        self.model = model
        self.is_available = True  # Tracks status

    @abstractmethod
    def calculate_rent(self, days):
        """Abstract method to be implemented by child classes."""
        pass



