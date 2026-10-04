from datetime import datetime, timedelta

now = datetime.now()

# 1. Subtract five days
print("5 days ago:", now - timedelta(days=5))

# 2. Yesterday, today, tomorrow
print("Yesterday:", (now - timedelta(days=1)).date())
print("Today:    ", now.date())
print("Tomorrow: ", (now + timedelta(days=1)).date())

# 3. Drop microseconds
print("No microseconds:", now.replace(microsecond=0))

# 4. Difference between two dates in seconds
d1 = datetime(2026, 1, 1, 12, 0, 0)
d2 = datetime(2026, 1, 3, 15, 30, 0)
print("Difference (s):", (d2 - d1).total_seconds())
