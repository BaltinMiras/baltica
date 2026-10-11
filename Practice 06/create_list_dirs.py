import os
from pathlib import Path

base = Path(__file__).parent / "demo_dirs"

# Create nested directories
os.makedirs(base / "a" / "b" / "c", exist_ok=True)
(base / "a" / "one.txt").write_text("1")
(base / "a" / "b" / "two.py").write_text("print(2)")
(base / "a" / "b" / "c" / "three.txt").write_text("3")

# List files and folders
print("listdir:", os.listdir(base / "a"))

# Find files by extension (recursive)
print(".txt files:", [p.name for p in base.rglob("*.txt")])

# getcwd / chdir
old = os.getcwd()
os.chdir(base)
print("cwd:", os.path.basename(os.getcwd()))
os.chdir(old)

# rmdir removes only EMPTY directories
os.mkdir(base / "empty")
os.rmdir(base / "empty")
print("empty dir removed")
try:
    os.rmdir(base / "a" / "b" / "c")
except OSError:
    print("rmdir failed: folder not empty")
