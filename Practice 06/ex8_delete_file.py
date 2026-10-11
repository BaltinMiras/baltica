import os
from pathlib import Path

path = input("File to delete (Enter = create demo file): ")
if not path:
    path = str(Path(__file__).parent / "to_delete.txt")
    Path(path).write_text("temp")

if not os.path.exists(path):
    print("Path does not exist")
elif not os.access(path, os.W_OK):
    print("No permission to delete")
else:
    os.remove(path)
    print("Deleted:", path)
