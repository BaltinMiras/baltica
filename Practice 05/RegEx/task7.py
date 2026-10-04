import re
# snake_case -> camelCase
def to_camel(s):
    return re.sub(r"_([a-z])", lambda m: m.group(1).upper(), s)
print(to_camel("snake_case_to_camel"))
