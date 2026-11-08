from connect import get_conn, run_sql_file

def show(rows):
    for r in rows:
        print(r)
    if not rows:
        print("(empty)")

def main():
    run_sql_file("functions.sql")
    run_sql_file("procedures.sql")
    page_size, page = 5, 0
    while True:
        cmd = input("\n1-search 2-upsert 3-bulk 4-page(n/p) 5-delete 0-exit > ").strip()
        with get_conn() as conn, conn.cursor() as cur:
            if cmd == "1":
                cur.execute("SELECT * FROM search_contacts(%s)", (input("Pattern: "),))
                show(cur.fetchall())
            elif cmd == "2":
                cur.execute("CALL upsert_contact(%s, %s)", (input("Name: "), input("Phone: ")))
            elif cmd == "3":
                names = input("Names (comma separated): ").split(",")
                phones = input("Phones (comma separated): ").split(",")
                cur.execute("CALL insert_many_contacts(%s, %s, %s)",
                            ([n.strip() for n in names], [p.strip() for p in phones], []))
                print("Incorrect:", cur.fetchone()[0])
            elif cmd == "4":
                while True:
                    cur.execute("SELECT * FROM get_contacts_page(%s, %s)", (page_size, page * page_size))
                    print(f"--- page {page + 1} ---")
                    show(cur.fetchall())
                    nav = input("n-next p-prev q-quit > ")
                    if nav == "n": page += 1
                    elif nav == "p": page = max(0, page - 1)
                    else: break
            elif cmd == "5":
                cur.execute("CALL delete_contact(%s)", (input("Name or phone: "),))
            elif cmd == "0":
                break

if __name__ == "__main__":
    main()
