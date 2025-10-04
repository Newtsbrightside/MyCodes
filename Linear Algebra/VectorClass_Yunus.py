import math

class Vector:
    def __init__(self, coordinates):
        # YOUR TASK HERE
        if isinstance(coordinates, (list, tuple)):
            self.coordinates = list(coordinates)
        else:
            # Handle single number case
            self.coordinates = [coordinates]

    # Instance method: magnitude
    def magnitude(self):
        # YOUR TASK HERE
        return math.sqrt(sum(coord ** 2 for coord in self.coordinates))

    # Instance method: normalize
    def normalize(self):
        # YOUR TASK HERE
        mag = self.magnitude()
        if mag == 0:
            return Vector([0] * len(self.coordinates))
        return Vector([coord / mag for coord in self.coordinates])

    # Class method: from list
    @classmethod
    def from_list(cls, lst):
        # YOUR TASK HERE
        return cls(lst)

    # Static method: dot product
    @staticmethod
    def dot_product(v1, v2):
       # YOUR TASK HERE
       if len(v1.coordinates) != len(v2.coordinates):
           raise ValueError("Vectors must have the same dimension")
       return sum(a * b for a, b in zip(v1.coordinates, v2.coordinates))

    # Operator overloading: addition
    def __add__(self, other):
        # YOUR TASK HERE
        if isinstance(other, Vector):
            if len(self.coordinates) != len(other.coordinates):
                raise ValueError("Vectors must have the same dimension")
            return Vector([a + b for a, b in zip(self.coordinates, other.coordinates)])
        return NotImplemented

    # Operator overloading: scalar multiplication
    def __mul__(self, scalar):
        # YOUR TASK HERE
        if isinstance(scalar, (int, float)):
            return Vector([coord * scalar for coord in self.coordinates])
        return NotImplemented

    # String representation
    def __str__(self):
        # YOUR TASK HERE
        return f"Vector({self.coordinates})"


# ================================
# Example usage (main demo)
# ================================
# Creating vectors
v1 = Vector([3, 4, 0])
v2 = Vector.from_list([1, 2, 3])

# Instance methods
print("Magnitude of v1:", v1.magnitude())       # 5.0
print("Normalized v2:", v2.normalize())         # Vector([...])

# Operator overloading
print("v1 + v2 =", v1 + v2)                     # Vector([4, 6, 3])
print("v1 * 2 =", v1 * 2)                       # Vector([6, 8, 0])

# Static method
print("Dot product:", Vector.dot_product(v1, v2))  # 11