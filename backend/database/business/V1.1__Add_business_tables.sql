/* Migration script to create all tables */


CREATE TABLE configuration (
    id SERIAL PRIMARY KEY,
    company_id INT NOT NULL,
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
    id SERIAL PRIMARY KEY,
    company_id INT NOT NULL,
    keyword VARCHAR NOT NULL,
    tags jsonb, -- Map ( entities:[sbi], categories:[fraud] );
    created_at TIMESTAMP WITH TIME ZONE DEFAULT now(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT now(),
    transaction_id SMALLINT
);

CREATE TABLE observer (
    id SERIAL PRIMARY KEY,
    company_id INT NOT NULL,
    name VARCHAR,
    observer_type SMALLINT, -- twitter, app_android, app_ios, youtube
    entity_id INT,
    tags VARCHAR[],
    is_enabled boolean DEFAULT TRUE,
    data jsonb, -- ( app_id, app_info);
    created_at TIMESTAMP WITH TIME ZONE DEFAULT now(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT now(),
    transaction_id SMALLINT
);

CREATE TABLE entity (
    id SERIAL PRIMARY KEY,
    company_id INT NOT NULL,
    name VARCHAR,
    simple_name VARCHAR,
    city VARCHAR,
    country VARCHAR,
    type VARCHAR,
    is_enabled boolean DEFAULT TRUE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT now(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT now(),
    transaction_id SMALLINT
);

-- access token refresh MECHANISM
CREATE TABLE vault (
    id SERIAL PRIMARY KEY,
    company_id INT NOT NULL,
    encrypted_value VARCHAR NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT now(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT now(),
    transaction_id SMALLINT
);
