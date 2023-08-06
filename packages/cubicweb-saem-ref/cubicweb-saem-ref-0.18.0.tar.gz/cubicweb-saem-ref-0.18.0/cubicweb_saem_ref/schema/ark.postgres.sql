--
-- Utilities to handle the "ark" table.
--

-- Return a part (name or qualifier) of an ARK identifier of `len` length with
-- `prefix` prefix and `control_char` trailing character.
CREATE OR REPLACE
FUNCTION gen_ark_part(len INTEGER, prefix TEXT, control_char TEXT)
RETURNS text AS $$
DECLARE
    result TEXT;
    letters TEXT;
    numbers TEXT;
    characters TEXT;
    next_char TEXT;
    tail TEXT;
    break_length INTEGER;
BEGIN
    ASSERT len > length(prefix) + length(control_char);
    letters := 'bcdfghjkmnpqrstvwxz';
    numbers := '0123456789';
    characters := letters || numbers;
    -- Length of "result" at which we break the loop.
    break_length = len - length(control_char);
    -- Start with "prefix".
    result := prefix;
    LOOP
        tail := substring(result, length(result) - 2, 3);
        -- No more than 3 consecutive consonants.
        IF tail ~ '([a-z]){3}' THEN
            next_char := random_char(numbers);
        ELSE
            next_char := random_char(characters);
        END IF;
        result := result || next_char;
        IF length(result) = break_length THEN
            EXIT;
        END IF;
    END LOOP;
    -- Add control character.
    RETURN result || control_char;
END;
$$ language 'plpgsql';

-- Return an random character within given string
CREATE OR REPLACE FUNCTION random_char(chars TEXT) RETURNS text AS $$
BEGIN
    RETURN substr(chars, (random() * (length(chars) -1) + 1)::INTEGER, 1);
END;
$$ language 'plpgsql';

-- Insert a record in "ark" table ensuring uniqueness constraints are
-- fulfilled.
CREATE OR REPLACE
FUNCTION gen_ark(naan INTEGER, len INTEGER, prefix TEXT, control_char TEXT, maxit INTEGER)
RETURNS TEXT AS $$
DECLARE
    ark_name TEXT;
    nit INTEGER;
BEGIN
    nit := 0;
    LOOP
        ASSERT nit < maxit,
            'ark generation loop exceeded maximum number of iterations: ' || maxit;
        nit := nit + 1;
        BEGIN
            INSERT INTO ark
                VALUES (naan, gen_ark_part(len, prefix, control_char), DEFAULT)
                RETURNING name INTO ark_name;
            RETURN ark_name;
        EXCEPTION
            WHEN unique_violation THEN
                -- Continue and try with another "name".
                NULL;
        END;
    END LOOP;
END;
$$ LANGUAGE plpgsql;

-- Insert a record in "ark" table from a "naan" value and a "base" identifier
-- using a qualifier.
CREATE OR REPLACE
FUNCTION gen_qualified_ark(naan_ INTEGER, base TEXT, len INTEGER, maxit INTEGER)
RETURNS TEXT AS $$
DECLARE
    ark_qualifier TEXT;
    nit INTEGER;
BEGIN
    PERFORM 1 FROM ark WHERE ark.name = base AND ark.qualifier = '';
    IF NOT FOUND THEN
        RAISE 'no ark record matching "%/%" found', naan_, base
        USING ERRCODE = 'invalid_parameter_value';
    END IF;
    nit := 0;
    LOOP
        ASSERT nit < maxit,
            'ark generation loop exceeded maximum number of iterations: ' || maxit;
        nit := nit + 1;
        BEGIN
            INSERT INTO ark
                VALUES (naan_, base, gen_ark_part(len, '', ''))
                RETURNING qualifier INTO ark_qualifier;
            RETURN ark_qualifier;
        EXCEPTION
            WHEN unique_violation THEN
                -- Continue and try with another "name".
                NULL;
        END;
    END LOOP;
END;
$$ LANGUAGE plpgsql;
