from pathlib import Path

f = Path(__file__).parent / "lines_demo.txt"
f.write_text("one\ntwo\nthree\n")

with open(f) as file:
    print("Lines:", sum(1 for _ in file))   # 3
