--liquibase formatted sql

--changeset girish:biz_ddl_001

CREATE TABLE configuration (
    identifier SERIAL PRIMARY KEY,
    company_id INT NOT NULL,
    observer_id INT NOT NULL,
    name VARCHAR NOT NULL,
    node_type SMALLINT,  -- observer|analyser|informer
    config_json jsonb, -- obsei parameters required
    vault_id INT,
    tags jsonb,
    is_enabled boolean DEFAULT TRUE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT now(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT now(),
    transaction_id SMALLINT
);

CREATE TABLE domain_dictionary (
    identifier SERIAL PRIMARY KEY,
    company_id INT NOT NULL,
    term VARCHAR NOT NULL,
    term_description VARCHAR,
    categories VARCHAR[],
    data jsonb,
    is_deleted boolean NULL DEFAULT false,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT now(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT now(),
    transaction_id SMALLINT,
    CONSTRAINT term_and_company UNIQUE (term, company_id)
);

CREATE TABLE observer (
    identifier SERIAL PRIMARY KEY,
    company_id INT NOT NULL,
    name VARCHAR,
    observer_type SMALLINT, -- twitter, app_android, app_ios, youtube
    entity_id INT,
    tags jsonb,
    is_enabled boolean DEFAULT TRUE,
    data jsonb, -- ( app_id, app_info);
    created_at TIMESTAMP WITH TIME ZONE DEFAULT now(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT now(),
    transaction_id SMALLINT,
    regulated_entity_type varchar[],
    is_deleted boolean DEFAULT FALSE
);

CREATE TABLE entity (
    identifier SERIAL PRIMARY KEY,
    company_id INT NOT NULL,
    name VARCHAR,
    simple_name VARCHAR,
    city VARCHAR,
    country VARCHAR,
    regulated_type VARCHAR[],
    is_enabled boolean DEFAULT TRUE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT now(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT now(),
    transaction_id SMALLINT,
    is_deleted boolean DEFAULT FALSE
);

-- access token refresh MECHANISM
CREATE TABLE vault (
    identifier SERIAL PRIMARY KEY,
    company_id INT NOT NULL,
    encrypted_value VARCHAR NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT now(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT now(),
    transaction_id SMALLINT
);

--rollback DROP TABLE configuration;
--rollback DROP TABLE domain_dictionary;
--rollback DROP TABLE observer;
--rollback DROP TABLE entity;
--rollback DROP TABLE vault;
