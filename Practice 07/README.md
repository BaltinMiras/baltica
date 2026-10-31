# Practice 07: Python & PostgreSQL — PhoneBook

## Requirements
- Python 3.9+
- PostgreSQL
- psycopg2-binary

## Setup

1. Create a PostgreSQL database named `phonebook`:

```sql
CREATE DATABASE phonebook;
```

2. Install the dependencies:

```bash
pip install -r requirements.txt
```

3. Configure the database connection using environment variables:

```bash
set DB_HOST=localhost
set DB_PORT=5432
set DB_NAME=phonebook
set DB_USER=postgres
set DB_PASSWORD=your_password
```

On macOS/Linux, use `export` instead of `set`.

4. Run the application:

```bash
python phonebook.py
```

The contacts table is created automatically when the application starts.

## Features
- Create and display contacts
- Import contacts from CSV
- Add contacts through the console
- Update a contact's first name or phone number
- Search by name or phone prefix
- Delete contacts by name or phone number

## CSV format

The CSV file must contain the columns `first_name` and `phone`.
The included `contacts.csv` file provides sample data.

## Project structure

```text
Practice7/
├── phonebook.py
├── config.py
├── connect.py
├── contacts.csv
├── requirements.txt
├── .env.example
└── README.md
```
