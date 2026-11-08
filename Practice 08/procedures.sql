-- 2. Insert new user, or update phone if the name already exists
CREATE OR REPLACE PROCEDURE upsert_contact(p_name VARCHAR, p_phone VARCHAR)
LANGUAGE plpgsql AS $$
BEGIN
    IF EXISTS (SELECT 1 FROM contacts WHERE name = p_name) THEN
        UPDATE contacts SET phone = p_phone WHERE name = p_name;
    ELSE
        INSERT INTO contacts(name, phone) VALUES (p_name, p_phone);
    END IF;
END;
$$;

-- 3. Bulk insert with phone validation; incorrect rows are returned via INOUT
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

-- 5. Delete by name or phone
CREATE OR REPLACE PROCEDURE delete_contact(p_value VARCHAR)
LANGUAGE plpgsql AS $$
BEGIN
    DELETE FROM contacts WHERE name = p_value OR phone = p_value;
END;
$$;
