import re
# split at uppercase letters
print(re.split(r"(?=[A-Z])", "SplitAtUpperCaseLetters")[1:])
