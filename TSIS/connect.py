import os
import psycopg2
from config import DB

def get_conn():
    return psycopg2.connect(**DB)

def run_sql_file(path):
    path = os.path.join(os.path.dirname(os.path.abspath(__file__)), path)
    with get_conn() as conn, conn.cursor() as cur, open(path, encoding="utf-8") as f:
        cur.execute(f.read())
