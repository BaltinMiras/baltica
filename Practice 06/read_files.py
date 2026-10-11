from pathlib import Path

folder = Path(__file__).parent / "demo"
folder.mkdir(exist_ok=True)
f = folder / "read_demo.txt"
f.write_text("apple\nbanana\ncherry\n")

with open(f) as file:
    print("read():", repr(file.read()))

with open(f) as file:
    print("readline():", repr(file.readline()))

with open(f) as file:
    print("readlines():", file.readlines())

with open(f) as file:           # best way for big files: loop over lines
    for line in file:
        print(line.strip())
