import shutil
from pathlib import Path

base = Path(__file__).parent / "demo_move"
src, dst = base / "src", base / "dst"
src.mkdir(parents=True, exist_ok=True)
dst.mkdir(exist_ok=True)

(src / "a.txt").write_text("A")
(src / "b.txt").write_text("B")

shutil.copy(src / "a.txt", dst / "a.txt")    # copy: stays in src
shutil.move(src / "b.txt", dst / "b.txt")    # move: removed from src

print("src:", sorted(p.name for p in src.iterdir()))
print("dst:", sorted(p.name for p in dst.iterdir()))
