--liquibase formatted sql

--changeset girish:core_ddl_002

ALTER TABLE tenant_master DROP COLUMN nile_org_id;

--rollback ALTER TABLE tenant_master ADD COLUMN nile_org_id VARCHAR;
