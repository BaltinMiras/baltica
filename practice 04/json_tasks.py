import json

with open("sample-data.json") as f:
    data = json.load(f)

print("Interface Status")
print("=" * 80)
print(f"{'DN':<50} {'Description':<20}  {'Speed':<6}  {'MTU':<6}")
print(f"{'-'*50} {'-'*20}  {'-'*6}  {'-'*6}")

for item in data["imdata"]:
    a = item["l1PhysIf"]["attributes"]
    print(f"{a['dn']:<50} {a['descr']:<20}  {a['speed']:<6}  {a['mtu']:<6}")
