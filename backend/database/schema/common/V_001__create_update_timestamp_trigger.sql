--liquibase formatted sql

-- can not use $$ because of liquibase parsing,
-- hence using single quote and escaping with two single quote inside string definition

--changeset girish:C001 context:create_trigger runAlways:true

CREATE OR REPLACE FUNCTION updated_timestamp_func()
RETURNS TRIGGER AS '
BEGIN
  NEW.updated_at = NOW();
  RETURN NEW;
END;
' LANGUAGE plpgsql;


DO '
DECLARE
    t text;
BEGIN
    FOR t IN
        SELECT table_name FROM information_schema.columns WHERE column_name = ''updated_at''
    LOOP
        EXECUTE format(''DROP TRIGGER IF EXISTS trigger_update_timestamp ON %I;
                    CREATE TRIGGER trigger_update_timestamp
                    BEFORE UPDATE ON %I
                    FOR EACH ROW EXECUTE PROCEDURE updated_timestamp_func();'', t,t);
    END loop;
END;
' language 'plpgsql';

--rollback DROP FUNCTION updated_timestamp_func CASCADE;
