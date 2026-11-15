-- ===== Practice 8 objects, adapted to the new schema (phones now live in `phones`) =====

-- Insert new contact, or update its (first) phone if the name already exists
CREATE OR REPLACE PROCEDURE upsert_contact(p_name VARCHAR, p_phone VARCHAR)
LANGUAGE plpgsql AS $$
DECLARE
    v_id INT;
BEGIN
    SELECT id INTO v_id FROM contacts WHERE name = p_name ORDER BY id LIMIT 1;
    IF v_id IS NULL THEN
        INSERT INTO contacts(name, group_id)
        VALUES (p_name, (SELECT id FROM groups WHERE name = 'Other')) RETURNING id INTO v_id;
        INSERT INTO phones(contact_id, phone, type) VALUES (v_id, p_phone, 'mobile');
    ELSE
        UPDATE phones SET phone = p_phone
        WHERE id = (SELECT min(id) FROM phones WHERE contact_id = v_id);
        IF NOT FOUND THEN
            INSERT INTO phones(contact_id, phone, type) VALUES (v_id, p_phone, 'mobile');
        END IF;
    END IF;
END;
$$;

-- Bulk insert with phone validation; incorrect rows are returned via INOUT
-- Valid phone: optional +, then 7-15 digits
CREATE OR REPLACE PROCEDURE insert_many_contacts(
    p_names  TEXT[],
    p_phones TEXT[],
    INOUT incorrect TEXT[] DEFAULT '{}'
)
LANGUAGE plpgsql AS $$
DECLARE
    i INT;
BEGIN
    incorrect := '{}';
    FOR i IN 1 .. COALESCE(array_length(p_names, 1), 0) LOOP
        IF p_phones[i] IS NOT NULL AND p_phones[i] ~ '^\+?[0-9]{7,15}$' THEN
            CALL upsert_contact(p_names[i], p_phones[i]);
        ELSE
            incorrect := incorrect || (p_names[i] || ': ' || COALESCE(p_phones[i], 'NULL'));
        END IF;
    END LOOP;
END;
$$;

-- Delete by name or by any of the contact's phones (phones cascade)
CREATE OR REPLACE PROCEDURE delete_contact(p_value VARCHAR)
LANGUAGE plpgsql AS $$
BEGIN
    DELETE FROM contacts
    WHERE name = p_value
       OR id IN (SELECT contact_id FROM phones WHERE phone = p_value);
END;
$$;

-- Pagination (same name and first two arguments as Practice 8; now returns full rows
-- and takes an optional sort: 'name', 'birthday', 'date', default = by id)
DROP FUNCTION IF EXISTS get_contacts_page(INT, INT);
CREATE OR REPLACE FUNCTION get_contacts_page(p_limit INT, p_offset INT, p_sort TEXT DEFAULT 'id')
RETURNS SETOF contacts_full AS $$
BEGIN
    RETURN QUERY
    SELECT v.* FROM contacts_full v
    ORDER BY CASE WHEN p_sort = 'name'     THEN v.name END,
             CASE WHEN p_sort = 'birthday' THEN v.birthday END NULLS LAST,
             CASE WHEN p_sort = 'date'     THEN v.created_at END,
             v.id
    LIMIT p_limit OFFSET p_offset;
END;
$$ LANGUAGE plpgsql;

-- ===== TSIS1 new objects =====

-- 1. Add a phone number to an existing contact
CREATE OR REPLACE PROCEDURE add_phone(p_contact_name VARCHAR, p_phone VARCHAR, p_type VARCHAR)
LANGUAGE plpgsql AS $$
DECLARE
    v_id INT;
BEGIN
    SELECT id INTO v_id FROM contacts WHERE name = p_contact_name ORDER BY id LIMIT 1;
    IF v_id IS NULL THEN
        RAISE EXCEPTION 'Contact "%" not found', p_contact_name;
    END IF;
    INSERT INTO phones(contact_id, phone, type) VALUES (v_id, p_phone, lower(p_type));
END;
$$;

-- 2. Move a contact to a group; the group is created if it does not exist
CREATE OR REPLACE PROCEDURE move_to_group(p_contact_name VARCHAR, p_group_name VARCHAR)
LANGUAGE plpgsql AS $$
DECLARE
    v_id  INT;
    v_gid INT;
BEGIN
    SELECT id INTO v_id FROM contacts WHERE name = p_contact_name ORDER BY id LIMIT 1;
    IF v_id IS NULL THEN
        RAISE EXCEPTION 'Contact "%" not found', p_contact_name;
    END IF;
    SELECT id INTO v_gid FROM groups WHERE lower(name) = lower(p_group_name);
    IF v_gid IS NULL THEN
        INSERT INTO groups(name) VALUES (p_group_name) RETURNING id INTO v_gid;
    END IF;
    UPDATE contacts SET group_id = v_gid WHERE id = v_id;
END;
$$;

-- 3. Pattern search over name, surname, email and ALL phones (replaces the Practice 8 version)
DROP FUNCTION IF EXISTS search_contacts(TEXT);
CREATE OR REPLACE FUNCTION search_contacts(p_query TEXT)
RETURNS SETOF contacts_full AS $$
BEGIN
    RETURN QUERY
    SELECT v.* FROM contacts_full v
    WHERE v.name    ILIKE '%' || p_query || '%'
       OR v.surname ILIKE '%' || p_query || '%'
       OR v.email   ILIKE '%' || p_query || '%'
       OR EXISTS (SELECT 1 FROM phones p
                  WHERE p.contact_id = v.id AND p.phone ILIKE '%' || p_query || '%')
    ORDER BY v.id;
END;
$$ LANGUAGE plpgsql;
