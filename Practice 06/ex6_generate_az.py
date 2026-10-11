import string
from pathlib import Path

folder = Path(__file__).parent / "letters"
folder.mkdir(exist_ok=True)

for ch in string.ascii_uppercase:
    (folder / f"{ch}.txt").write_text("")

print(len(list(folder.glob("*.txt"))), "files created")   # 26
