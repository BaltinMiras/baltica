CREATE TABLE IF NOT EXISTS contacts (
    id      SERIAL PRIMARY KEY,
    name    VARCHAR(50) NOT NULL,
    surname VARCHAR(50) NOT NULL DEFAULT '',
    phone   VARCHAR(20) NOT NULL
);

-- 1. Pattern search: part of name, surname or phone
CREATE OR REPLACE FUNCTION search_contacts(p TEXT)
RETURNS TABLE(id INT, name VARCHAR, surname VARCHAR, phone VARCHAR) AS $$
BEGIN
    RETURN QUERY
    SELECT c.id, c.name, c.surname, c.phone FROM contacts c
    WHERE c.name ILIKE '%' || p || '%'
       OR c.surname ILIKE '%' || p || '%'
       OR c.phone ILIKE '%' || p || '%'
    ORDER BY c.id;
END;
$$ LANGUAGE plpgsql;

-- 4. Pagination
CREATE OR REPLACE FUNCTION get_contacts_page(p_limit INT, p_offset INT)
RETURNS TABLE(id INT, name VARCHAR, surname VARCHAR, phone VARCHAR) AS $$
BEGIN
    RETURN QUERY
    SELECT c.id, c.name, c.surname, c.phone FROM contacts c
    ORDER BY c.id LIMIT p_limit OFFSET p_offset;
END;
$$ LANGUAGE plpgsql;
