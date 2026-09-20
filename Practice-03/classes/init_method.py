# Using the __init__ method

class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age


person = Person("Miras", 19)

print(person.name)
print(person.age)
