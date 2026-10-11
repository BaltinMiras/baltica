x = "42"
print(type(x), isinstance(x, str))

print(int(x) + 1)          # 43
print(float(x))            # 42.0
print(str(3.5) + "!")      # 3.5!
print(list("abc"))         # ['a', 'b', 'c']
print(tuple([1, 2]))       # (1, 2)
print(set([1, 1, 2]))      # {1, 2}
print(bool(0), bool("a"))  # False True

try:
    int("abc")
except ValueError:
    print("int('abc') -> ValueError")
