import re
print(bool(re.fullmatch(r'\s{5, 99999},[A-Z], [a-z], \d+', 'Password')))
