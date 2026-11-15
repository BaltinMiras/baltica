-- TSIS1 schema. Safe to run repeatedly; also migrates a Practice 8 database.

CREATE TABLE IF NOT EXISTS groups (
    id   SERIAL PRIMARY KEY,
    name VARCHAR(50) UNIQUE NOT NULL
);
INSERT INTO groups(name) VALUES ('Family'), ('Work'), ('Friend'), ('Other')
ON CONFLICT (name) DO NOTHING;

CREATE TABLE IF NOT EXISTS contacts (
    id      SERIAL PRIMARY KEY,
    name    VARCHAR(50) NOT NULL,
    surname VARCHAR(50) NOT NULL DEFAULT ''
);

ALTER TABLE contacts
    ADD COLUMN IF NOT EXISTS email      VARCHAR(100),
    ADD COLUMN IF NOT EXISTS birthday   DATE,
    ADD COLUMN IF NOT EXISTS group_id   INTEGER REFERENCES groups(id),
    ADD COLUMN IF NOT EXISTS created_at TIMESTAMP NOT NULL DEFAULT now();

CREATE TABLE IF NOT EXISTS phones (
    id         SERIAL PRIMARY KEY,
    contact_id INTEGER REFERENCES contacts(id) ON DELETE CASCADE,
    phone      VARCHAR(20) NOT NULL,
    type       VARCHAR(10) NOT NULL DEFAULT 'mobile' CHECK (type IN ('home', 'work', 'mobile'))
);

-- Practice 8 stored one phone in contacts.phone: move it to the phones table, then drop it.
DO $$
BEGIN
    IF EXISTS (SELECT 1 FROM information_schema.columns
               WHERE table_name = 'contacts' AND column_name = 'phone') THEN
        INSERT INTO phones(contact_id, phone, type)
        SELECT id, phone, 'mobile' FROM contacts WHERE phone IS NOT NULL AND phone <> '';
        ALTER TABLE contacts DROP COLUMN phone;
    END IF;
END $$;

UPDATE contacts SET group_id = (SELECT id FROM groups WHERE name = 'Other') WHERE group_id IS NULL;

-- One row per contact with group name and all phones; used by the console and the functions.
CREATE OR REPLACE VIEW contacts_full AS
SELECT c.id, c.name, c.surname, c.email, c.birthday, g.name AS group_name, c.created_at,
       COALESCE(string_agg(p.type || ': ' || p.phone, ', ' ORDER BY p.id), '') AS phones
FROM contacts c
LEFT JOIN groups g ON g.id = c.group_id
LEFT JOIN phones p ON p.contact_id = c.id
GROUP BY c.id, g.name;
