--liquibase formatted sql

--changeset girish:core_ddl_003

CREATE TABLE api_auth_master (
    identifier UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
	tenant_ids UUID[] NOT NULL,
    name VARCHAR NOT NULL,
	hashed_key VARCHAR NOT NULL,
    is_enabled boolean DEFAULT TRUE,
	is_deleted boolean NULL DEFAULT FALSE,
	created_at TIMESTAMP WITH TIME ZONE DEFAULT now(),
	updated_at TIMESTAMP WITH TIME ZONE DEFAULT now()
);

--rollback DROP TABLE api_auth_master;
