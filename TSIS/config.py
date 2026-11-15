import os

# Password comes from the environment so it never gets committed to GitHub:
#   Windows: set DB_PASSWORD=...     Linux/macOS: export DB_PASSWORD=...
DB = dict(host=os.getenv("DB_HOST", "localhost"), dbname=os.getenv("DB_NAME", "phonebook"),
          user=os.getenv("DB_USER", "postgres"), password=os.getenv("DB_PASSWORD", ""),
          port=int(os.getenv("DB_PORT", "5432")))
