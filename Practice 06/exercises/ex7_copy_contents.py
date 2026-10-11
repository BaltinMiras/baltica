from pathlib import Path

folder = Path(__file__).parent
src, dst = folder / "source_demo.txt", folder / "copy_demo.txt"
src.write_text("hello\nworld\n")

with open(src) as fin, open(dst, "w") as fout:
    fout.write(fin.read())

print(dst.read_text())
