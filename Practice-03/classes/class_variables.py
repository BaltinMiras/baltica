# Class variable

class Person:
    species = "Human"

    def __init__(self, name):
        self.name = name


person1 = Person("Miras")
person2 = Person("Mari")

print(person1.name)
print(person1.species)

print(person2.name)
print(person2.species)
