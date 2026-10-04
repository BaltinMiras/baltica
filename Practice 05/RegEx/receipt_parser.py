import re
import json

with open("raw.txt", encoding="utf-8") as f:
    text = f.read()

def num(s):
    """'1 200,00' -> 1200.0"""
    return float(re.sub(r"\s", "", s).replace(",", "."))

# 1-2. Products: name, qty x price, line total
item_re = r"^\d+\.\n(.+)\n([\d\s]+,\d{3}) x ([\d\s]+,\d{2})\n([\d\s]+,\d{2})\nСтоимость"
items = [
    {"name": n.strip(), "qty": num(q), "price": num(p), "total": num(t)}
    for n, q, p, t in re.findall(item_re, text, re.MULTILINE)
]

# 3. Total: calculated vs printed
calculated = sum(i["total"] for i in items)
printed = num(re.search(r"ИТОГО:\n([\d\s]+,\d{2})", text).group(1))

# 4. Date and time
date, time = re.search(r"Время: (\d{2}\.\d{2}\.\d{4}) (\d{2}:\d{2}:\d{2})", text).groups()

# 5. Payment method
payment = re.search(r"^(.+):\n[\d\s]+,\d{2}\nИТОГО", text, re.MULTILINE).group(1)

# 6. Structured output
result = {
    "date": date,
    "time": time,
    "payment_method": payment,
    "items": items,
    "calculated_total": calculated,
    "printed_total": printed,
}
print(json.dumps(result, ensure_ascii=False, indent=2))
print("\nAll prices:", [i["total"] for i in items])
