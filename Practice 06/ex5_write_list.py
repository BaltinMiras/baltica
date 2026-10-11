from pathlib import Path

items = ["apple", "banana", "cherry"]
f = Path(__file__).parent / "list_demo.txt"

with open(f, "w") as file:
    for item in items:
        file.write(item + "\n")

print(f.read_text())
