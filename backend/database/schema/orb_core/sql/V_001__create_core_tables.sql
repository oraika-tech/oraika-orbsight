--liquibase formatted sql

--changeset girish:core_ddl_001

CREATE TABLE tenant_master (
    identifier UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
    nile_org_id VARCHAR,
    name VARCHAR NOT NULL,
    code VARCHAR NOT NULL, -- unique name for all internal purpose
    type SMALLINT NOT NULL, -- CORPORATE | GOV | INDIVIDUAL
    is_enabled boolean DEFAULT TRUE,
    is_deleted boolean DEFAULT FALSE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT now(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT now(),
    CONSTRAINT tenant_code UNIQUE (code)
);

CREATE TABLE tenant_global_config (
    identifier UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
    tenant_id UUID NOT NULL,
    config_key VARCHAR NOT NULL,
    config_value jsonb NOT NULL
);

CREATE TABLE user_master (
    identifier UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
	tenant_ids UUID[] NOT NULL,
    name VARCHAR NOT NULL,
	email VARCHAR NOT NULL UNIQUE,
	hash_password VARCHAR NOT NULL,
    is_email_verified BOOLEAN DEFAULT FALSE,
    is_enabled boolean DEFAULT TRUE,
	is_deleted boolean NULL DEFAULT FALSE,
	created_at TIMESTAMP WITH TIME ZONE DEFAULT now(),
	updated_at TIMESTAMP WITH TIME ZONE DEFAULT now()
);

--rollback DROP TABLE tenant_global_config;
--rollback DROP TABLE tenant;
--rollback DROP TABLE user_auth;
