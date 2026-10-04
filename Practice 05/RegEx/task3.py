import re
# lowercase letters joined with underscore
text = "hello_world, foo_bar_baz, Not_this, ok"
print(re.findall(r"\b[a-z]+(?:_[a-z]+)+\b", text))
