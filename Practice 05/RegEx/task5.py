import re
# 'a' followed by anything, ending in 'b'
for s in ["ab", "a123b", "acb!", "ba"]:
    print(s, bool(re.fullmatch(r"a.*b", s)))
