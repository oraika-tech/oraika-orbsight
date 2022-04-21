--liquibase formatted sql

--changeset girish:biz_ddl_002

ALTER TABLE domain_dictionary RENAME TO taxonomy;

ALTER TABLE taxonomy RENAME COLUMN data TO taxonomy_type;

--rollback ALTER TABLE taxonomy RENAME COLUMN taxonomy_type TO data;
--rollback ALTER TABLE taxonomy RENAME TO domain_dictionary;
