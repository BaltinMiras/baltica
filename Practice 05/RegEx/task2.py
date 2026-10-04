import re
# 'a' followed by two to three 'b'
for s in ["a", "ab", "abb", "abbb", "abbbb"]:
    print(s, bool(re.fullmatch(r"ab{2,3}", s)))
