import re
# 'a' followed by zero or more 'b'
for s in ["a", "ab", "abbb", "b", "ac"]:
    print(s, bool(re.fullmatch(r"ab*", s)))
