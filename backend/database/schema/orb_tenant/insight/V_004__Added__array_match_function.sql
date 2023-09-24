--liquibase formatted sql

--changeset girish:insight_ddl_004
CREATE OR REPLACE FUNCTION array_match(array_1 text[], array_2 text[])
RETURNS BOOLEAN
AS '
BEGIN
    IF ''*'' = ANY(array_2) THEN
        RETURN true;
    ELSE
        RETURN array_1 && array_2;
    END IF;
END;
'
LANGUAGE plpgsql;

--rollback DROP FUNCTION array_match;
