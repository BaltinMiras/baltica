import psycopg2
from config import DB_CONFIG


def get_connection():
    return psycopg2.connect(**DB_CONFIG)


def create_table():
    query = """
        CREATE TABLE IF NOT EXISTS contacts (
            id SERIAL PRIMARY KEY,
            first_name VARCHAR(100) NOT NULL,
            phone VARCHAR(30) NOT NULL UNIQUE
        );
    """

    with get_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute(query)
