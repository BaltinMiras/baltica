# Using lambda with sorted()

students = [
    ("Miras", 19),
    ("Maria", 18),
    ("Darkhan", 23)
]

sorted_students = sorted(students, key=lambda student: student[1])

print(sorted_students)
