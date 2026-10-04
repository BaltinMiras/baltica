import re
# camelCase -> snake_case
def to_snake(s):
    return re.sub(r"(?<!^)(?=[A-Z])", "_", s).lower()
print(to_snake("camelCaseToSnakeCase"))
