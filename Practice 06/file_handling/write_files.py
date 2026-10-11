from pathlib import Path

folder = Path(__file__).parent / "demo"
folder.mkdir(exist_ok=True)
f = folder / "notes.txt"

# 1. Create file and write data ("w" overwrites)
with open(f, "w") as file:
    file.write("Line 1\nLine 2\n")

# 2. Append new lines ("a" adds to the end)
with open(f, "a") as file:
    file.write("Line 3\n")

# 3. "x" creates a file, fails if it already exists
try:
    with open(f, "x") as file:
        file.write("never written")
except FileExistsError:
    print("x mode: file already exists")

# 4. Verify content
print(f.read_text())
