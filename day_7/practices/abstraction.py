from abc import abstractmethod, ABC

class Shape(ABC):

    @abstractmethod
    def area(self):
        pass

    @abstractmethod
    def perimeter(self):
        pass


class Circle(Shape):

    def __init__(self,radius):
        self.radius = radius

    def area(self):
        return 3.14159 * self.radius ** 2
    
    def circle(self):
        return 3.14159 * self.radius
    
circle = Circle(5)
print(f"Area: {circle.area()}")
print(f"Perimeter: {circle.perimeter()}")


