import re
# insert spaces between words starting with capital letters
print(re.sub(r"(?<!^)(?=[A-Z])", " ", "InsertSpacesBetweenWords"))
