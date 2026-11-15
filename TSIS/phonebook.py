import csv
import json
import psycopg2
from connect import get_conn, run_sql_file

PAGE_SIZE = 5
SORTS = {"name": "name, id", "birthday": "birthday NULLS LAST, id", "date": "created_at, id"}


def show(rows):
    for id_, name, surname, email, bday, group, added, phones in rows:
        print(f"[{id_}] {name} {surname}".rstrip(),
              f"| {email or '-'} | {bday or '-'} | {group} | {phones or '-'} | added {added:%Y-%m-%d}")
    if not rows:
        print("(empty)")


def ask_sort():
    s = input("Sort by name / birthday / date (Enter = none): ").strip().lower()
    return s if s in SORTS else ""


def listing(cur, source, args):
    """Run SELECT * on a view/function, with the user's chosen sort."""
    cur.execute(f"SELECT * FROM {source} ORDER BY {SORTS.get(ask_sort(), 'id')}", args)
    show(cur.fetchall())


# ---------- search / filter / pagination ----------
def search(cur):
    listing(cur, "search_contacts(%s)", (input("Search (name/surname/email/phone): "),))


def by_group(cur):
    cur.execute("SELECT name FROM groups ORDER BY id")
    print("Groups:", ", ".join(r[0] for r in cur.fetchall()))
    listing(cur, "contacts_full WHERE lower(group_name) = lower(%s)", (input("Group: ").strip(),))


def by_email(cur):
    listing(cur, "contacts_full WHERE email ILIKE %s", (f"%{input('Email contains: ').strip()}%",))


def browse(cur):
    sort, page = ask_sort() or "id", 0
    while True:
        cur.execute("SELECT * FROM get_contacts_page(%s, %s, %s)", (PAGE_SIZE, page * PAGE_SIZE, sort))
        rows = cur.fetchall()
        if not rows and page > 0:
            page -= 1
            print("No more pages.")
            continue
        print(f"--- page {page + 1} ---")
        show(rows)
        nav = input("next / prev / quit > ").strip().lower()
        if nav in ("next", "n"):
            page += 1
        elif nav in ("prev", "p"):
            page = max(0, page - 1)
        elif nav in ("quit", "q"):
            break


# ---------- add / modify ----------
def save_contact(cur, r):
    """Insert a contact dict, or ask skip/overwrite if the name already exists. True if saved."""
    if not r.get("name"):
        raise ValueError("name is required")
    cur.execute("SELECT id FROM contacts WHERE name = %s ORDER BY id LIMIT 1", (r["name"],))
    row = cur.fetchone()
    fields = (r.get("surname") or "", r.get("email") or None, r.get("birthday") or None)
    if row:
        if input(f'"{r["name"]}" already exists - skip or overwrite? [s/o] ').strip().lower() != "o":
            return False
        cur.execute("UPDATE contacts SET surname = %s, email = %s, birthday = %s WHERE id = %s",
                    fields + (row[0],))
        cur.execute("DELETE FROM phones WHERE contact_id = %s", (row[0],))
    else:
        cur.execute("INSERT INTO contacts(name, surname, email, birthday) VALUES (%s, %s, %s, %s)",
                    (r["name"],) + fields)
    cur.execute("CALL move_to_group(%s, %s)", (r["name"], r.get("group") or "Other"))
    for ph in r.get("phones", []):
        cur.execute("CALL add_phone(%s, %s, %s)", (r["name"], ph["phone"], ph.get("type") or "mobile"))
    return True


def import_records(cur, records):
    ok = skipped = failed = 0
    for r in records:
        cur.execute("SAVEPOINT rec")  # one bad record must not abort the whole import
        try:
            if save_contact(cur, r):
                ok += 1
            else:
                skipped += 1
            cur.execute("RELEASE SAVEPOINT rec")
        except Exception as e:
            cur.execute("ROLLBACK TO SAVEPOINT rec")
            failed += 1
            print(f"Failed '{r.get('name')}': {getattr(getattr(e, 'diag', None), 'message_primary', None) or e}")
    print(f"Saved {ok}, skipped {skipped}, failed {failed}")


def add_contact(cur):
    prompts = {"name": "Name", "surname": "Surname", "email": "Email",
               "birthday": "Birthday (YYYY-MM-DD)", "group": "Group (Family/Work/Friend/Other)"}
    r = {k: input(f"{p}: ").strip() for k, p in prompts.items()}
    phone = input("Phone: ").strip()
    r["phones"] = [{"phone": phone, "type": input("Type (home/work/mobile): ").strip().lower()}] if phone else []
    import_records(cur, [r])


def add_phone(cur):
    cur.execute("CALL add_phone(%s, %s, %s)", (input("Contact name: "), input("Phone: "),
                                               input("Type (home/work/mobile): ").strip().lower()))


def move_group(cur):
    cur.execute("CALL move_to_group(%s, %s)", (input("Contact name: "), input("Group: ").strip()))


def delete(cur):
    cur.execute("CALL delete_contact(%s)", (input("Name or phone: "),))


def bulk(cur):
    names = [n.strip() for n in input("Names (comma separated): ").split(",")]
    phones = [p.strip() for p in input("Phones (comma separated): ").split(",")]
    cur.execute("CALL insert_many_contacts(%s, %s, %s)", (names, phones, []))
    print("Incorrect:", cur.fetchone()[0])


# ---------- import / export ----------
def import_csv(cur):
    """CSV columns: name,surname,email,birthday,group,phone,phone_type (one phone per row)."""
    path = input("CSV file [contacts.csv]: ").strip() or "contacts.csv"
    with open(path, newline="", encoding="utf-8-sig") as f:
        records = []
        for row in csv.DictReader(f):
            row = {k.strip(): (v or "").strip() for k, v in row.items() if k}
            phone = row.pop("phone", "")
            ptype = row.pop("phone_type", "").lower()
            row["phones"] = [{"phone": phone, "type": ptype}] if phone else []
            records.append(row)
    import_records(cur, records)


def export_json(cur):
    path = input("JSON file [contacts.json]: ").strip() or "contacts.json"
    cur.execute("""
        SELECT c.name, c.surname, c.email, c.birthday, g.name,
               COALESCE((SELECT json_agg(json_build_object('phone', p.phone, 'type', p.type) ORDER BY p.id)
                         FROM phones p WHERE p.contact_id = c.id), '[]')
        FROM contacts c LEFT JOIN groups g ON g.id = c.group_id ORDER BY c.id""")
    data = [dict(name=n, surname=s, email=e, birthday=str(b) if b else None, group=g, phones=ph)
            for n, s, e, b, g, ph in cur.fetchall()]
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    print(f"Exported {len(data)} contacts to {path}")


def import_json(cur):
    path = input("JSON file [contacts.json]: ").strip() or "contacts.json"
    with open(path, encoding="utf-8") as f:
        import_records(cur, json.load(f))


MENU = {
    "1": ("Search (name / surname / email / any phone)", search),
    "2": ("Filter by group", by_group),
    "3": ("Search by email", by_email),
    "4": ("Browse pages (next / prev / quit)", browse),
    "5": ("Add / update contact", add_contact),
    "6": ("Add phone to contact", add_phone),
    "7": ("Move contact to group", move_group),
    "8": ("Delete by name or phone", delete),
    "9": ("Bulk add (name + phone, validated)", bulk),
    "10": ("Import CSV", import_csv),
    "11": ("Export JSON", export_json),
    "12": ("Import JSON", import_json),
    "0": ("Exit", None),
}


def main():
    run_sql_file("schema.sql")
    run_sql_file("procedures.sql")
    conn = get_conn()
    while True:
        print()
        for key, (label, _) in MENU.items():
            print(f"{key:>2} - {label}")
        cmd = input("> ").strip()
        if cmd == "0":
            break
        if cmd not in MENU:
            print("Unknown command")
            continue
        try:
            with conn, conn.cursor() as cur:  # commits on success, rolls back on error
                MENU[cmd][1](cur)
        except psycopg2.Error as e:
            print("DB error:", e.diag.message_primary or e)
        except (OSError, ValueError) as e:  # missing file, bad JSON
            print("Error:", e)
    conn.close()


if __name__ == "__main__":
    main()
