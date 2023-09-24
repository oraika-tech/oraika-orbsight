--liquibase formatted sql

--changeset girish:cmp_ddl_001

CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

--rollback DROP EXTENSION "uuid-ossp";
