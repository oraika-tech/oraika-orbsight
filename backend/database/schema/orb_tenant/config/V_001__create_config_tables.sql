--liquibase formatted sql

--changeset girish:config_ddl_001

CREATE TABLE tenant_config (
    identifier UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
    ----
    config_key VARCHAR NOT NULL,
    config_value jsonb NOT NULL,
    ----
    is_enabled boolean DEFAULT TRUE,
    is_deleted boolean DEFAULT FALSE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT now(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT now(),
    transaction_id SMALLINT
);

CREATE TABLE config_entity (
    identifier UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
    ----
    name VARCHAR NOT NULL,
    tags VARCHAR[] NOT NULL DEFAULT '{}',
    ----
    is_enabled boolean DEFAULT TRUE,
    is_deleted boolean DEFAULT FALSE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT now(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT now(),
    transaction_id SMALLINT
);
CREATE INDEX config_entity_name_idx ON config_entity USING hash( name );

CREATE TABLE config_observer (
    identifier UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
    ----
    name VARCHAR NOT NULL,
    type SMALLINT NOT NULL, -- twitter, app_android, app_ios, youtube
    entity_id UUID NOT NULL,
    tags VARCHAR[] NOT NULL DEFAULT '{}',
    config_data jsonb, -- (app_id, app_info);
    ----
    is_enabled boolean DEFAULT TRUE,
    is_deleted boolean DEFAULT FALSE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT now(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT now(),
    transaction_id SMALLINT
);
CREATE INDEX config_observer_type_idx ON config_observer USING hash( type );

CREATE TABLE config_taxonomy (
    identifier UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
    ----
    keyword VARCHAR NOT NULL UNIQUE,
    term VARCHAR NOT NULL,
    description VARCHAR,
    categories VARCHAR[] NOT NULL DEFAULT '{}',
    tags VARCHAR[] NOT NULL DEFAULT '{}',
    ----
    is_enabled boolean DEFAULT TRUE,
    is_deleted boolean NULL DEFAULT FALSE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT now(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT now(),
    transaction_id SMALLINT
);

CREATE TABLE config_category (
    identifier UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
    ----
	name VARCHAR NOT NULL UNIQUE,
    ----
    is_enabled boolean DEFAULT TRUE,
    is_deleted boolean NULL DEFAULT FALSE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT now(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT now(),
    transaction_id SMALLINT
);

--rollback DROP TABLE config_category;
--rollback DROP TABLE config_taxonomy;
--rollback DROP TABLE config_observer;
--rollback DROP TABLE config_entity;
--rollback DROP TABLE tenant_config;
