import os
import shutil
from pathlib import Path

folder = Path(__file__).parent / "demo"
folder.mkdir(exist_ok=True)
src = folder / "data.txt"
src.write_text("important data\n")

# Copy and backup
shutil.copy(src, folder / "data_copy.txt")
shutil.copy2(src, folder / "data_backup.txt")    # also keeps metadata

# Safe delete: check first
for name in ["data_copy.txt", "missing.txt"]:
    p = folder / name
    if p.exists():
        os.remove(p)
        print("Deleted:", name)
    else:
        print("Not found:", name)

print(sorted(os.listdir(folder)))
