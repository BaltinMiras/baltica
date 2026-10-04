import re
# one uppercase letter followed by lowercase letters
text = "Hello World from Python and JSON"
print(re.findall(r"[A-Z][a-z]+", text))
