--liquibase formatted sql

--changeset girish:core_ddl_005

ALTER TABLE tenant_global_config 
ADD CONSTRAINT tenant_config_key_unique 
UNIQUE (tenant_id, config_key);

--rollback ALTER TABLE tenant_global_config DROP CONSTRAINT tenant_config_key_unique;