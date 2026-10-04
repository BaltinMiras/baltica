import math

# 1. Degrees to radians
deg = float(input("Input degree: "))
print("Output radian:", round(math.radians(deg), 6))

# 2. Trapezoid area
h = float(input("Height: "))
b1 = float(input("Base, first value: "))
b2 = float(input("Base, second value: "))
print("Expected Output:", (b1 + b2) / 2 * h)

# 3. Regular polygon area
n = int(input("Input number of sides: "))
s = float(input("Input the length of a side: "))
print("The area of the polygon is:", round(n * s ** 2 / (4 * math.tan(math.pi / n))))

# 4. Parallelogram area
base = float(input("Length of base: "))
height = float(input("Height of parallelogram: "))
print("Expected Output:", base * height)
