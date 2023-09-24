
-- Automate this

CREATE USER view_reader WITH encrypted password 'password';
GRANT CONNECT ON DATABASE orb_tenant_rbi TO view_reader;
\c orb_tenant_rbi
CREATE SCHEMA views_only;
GRANT USAGE ON SCHEMA views_only TO view_reader;
GRANT SELECT ON views_only.processed_data_view_v1 TO view_reader;
