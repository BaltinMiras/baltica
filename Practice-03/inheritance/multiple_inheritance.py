# Multiple inheritance

class Father:
    def drive(self):
        print("Father can drive")


class Mother:
    def cook(self):
        print("Mother can cook")


class Child(Father, Mother):
    pass


child = Child()

child.drive()
child.cook()
