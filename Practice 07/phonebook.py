import csv
import os
import psycopg2

from connect import create_table, get_connection


def add_contact(first_name, phone):
    query = """
        INSERT INTO contacts (first_name, phone)
        VALUES (%s, %s)
        ON CONFLICT (phone) DO NOTHING;
    """
    with get_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute(query, (first_name.strip(), phone.strip()))
            return cursor.rowcount > 0


def import_from_csv(filename):
    if not os.path.exists(filename):
        print("CSV file was not found.")
        return

    added = 0
    skipped = 0

    with open(filename, newline="", encoding="utf-8-sig") as file:
        reader = csv.DictReader(file)
        if not reader.fieldnames or not {"first_name", "phone"}.issubset(reader.fieldnames):
            print("CSV must contain columns: first_name, phone.")
            return

        for row in reader:
            name = (row.get("first_name") or "").strip()
            phone = (row.get("phone") or "").strip()

            if not name or not phone:
                skipped += 1
                continue

            if add_contact(name, phone):
                added += 1
            else:
                skipped += 1

    print(f"Import finished. Added: {added}; skipped: {skipped}.")


def show_contacts(rows):
    if not rows:
        print("No contacts found.")
        return

    print("\nID | Name | Phone")
    print("-" * 40)
    for contact_id, first_name, phone in rows:
        print(f"{contact_id} | {first_name} | {phone}")


def get_all_contacts():
    with get_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute(
                "SELECT id, first_name, phone FROM contacts ORDER BY first_name;"
            )
            return cursor.fetchall()


def search_contacts():
    print("1. Search by name")
    print("2. Search by phone prefix")
    choice = input("Choose search type: ").strip()

    if choice == "1":
        value = input("Enter name: ").strip()
        query = """
            SELECT id, first_name, phone
            FROM contacts
            WHERE first_name ILIKE %s
            ORDER BY first_name;
        """
        parameter = (f"%{value}%",)
    elif choice == "2":
        value = input("Enter phone prefix: ").strip()
        query = """
            SELECT id, first_name, phone
            FROM contacts
            WHERE phone LIKE %s
            ORDER BY first_name;
        """
        parameter = (f"{value}%",)
    else:
        print("Invalid search option.")
        return

    with get_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute(query, parameter)
            show_contacts(cursor.fetchall())


def update_contact():
    phone = input("Enter the current phone number: ").strip()

    print("1. Update first name")
    print("2. Update phone number")
    choice = input("Choose what to update: ").strip()

    if choice == "1":
        value = input("Enter the new first name: ").strip()
        if not value:
            print("Name cannot be empty.")
            return
        query = "UPDATE contacts SET first_name = %s WHERE phone = %s;"
    elif choice == "2":
        value = input("Enter the new phone number: ").strip()
        if not value:
            print("Phone cannot be empty.")
            return
        query = "UPDATE contacts SET phone = %s WHERE phone = %s;"
    else:
        print("Invalid option.")
        return

    try:
        with get_connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute(query, (value, phone))
                if cursor.rowcount:
                    print("Contact updated successfully.")
                else:
                    print("Contact not found.")
    except psycopg2.IntegrityError:
        print("This phone number is already used by another contact.")


def delete_contact():
    print("1. Delete by name")
    print("2. Delete by phone number")
    choice = input("Choose deletion method: ").strip()

    if choice == "1":
        value = input("Enter the name: ").strip()
        query = "DELETE FROM contacts WHERE first_name ILIKE %s;"
        parameter = (value,)
    elif choice == "2":
        value = input("Enter the phone number: ").strip()
        query = "DELETE FROM contacts WHERE phone = %s;"
        parameter = (value,)
    else:
        print("Invalid option.")
        return

    with get_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute(query, parameter)
            print(f"Deleted contacts: {cursor.rowcount}")


def main():
    try:
        create_table()
        print("PhoneBook database is ready.")

        while True:
            print("\n===== PHONEBOOK =====")
            print("1. Show all contacts")
            print("2. Add a contact")
            print("3. Import contacts from CSV")
            print("4. Search contacts")
            print("5. Update a contact")
            print("6. Delete a contact")
            print("0. Exit")

            choice = input("Choose an option: ").strip()

            try:
                if choice == "1":
                    show_contacts(get_all_contacts())
                elif choice == "2":
                    name = input("Enter first name: ").strip()
                    phone = input("Enter phone number: ").strip()
                    if not name or not phone:
                        print("Name and phone cannot be empty.")
                    elif add_contact(name, phone):
                        print("Contact added successfully.")
                    else:
                        print("A contact with this phone number already exists.")
                elif choice == "3":
                    filename = input("Enter CSV filename [contacts.csv]: ").strip()
                    import_from_csv(filename or "contacts.csv")
                elif choice == "4":
                    search_contacts()
                elif choice == "5":
                    update_contact()
                elif choice == "6":
                    delete_contact()
                elif choice == "0":
                    print("Goodbye.")
                    break
                else:
                    print("Invalid option. Try again.")
            except psycopg2.Error as error:
                print(f"Database error: {error}")

    except psycopg2.OperationalError:
        print("Could not connect to PostgreSQL. Check your database settings.")


if __name__ == "__main__":
    main()
