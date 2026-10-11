names = ["Ali", "Dana", "Sam"]
scores = [85, 60, 90]

for i, name in enumerate(names, start=1):
    print(i, name)

for name, score in zip(names, scores):
    print(name, score)

print(dict(zip(names, scores)))
