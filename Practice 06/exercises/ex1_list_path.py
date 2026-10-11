import os

path = input("Path (Enter = current): ") or "."
items = os.listdir(path)

dirs = [i for i in items if os.path.isdir(os.path.join(path, i))]
files = [i for i in items if os.path.isfile(os.path.join(path, i))]

print("Directories:", dirs)
print("Files:", files)
print("All:", items)
