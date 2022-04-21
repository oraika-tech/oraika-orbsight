--liquibase formatted sql

--changeset girish:rbi_ddl_001


CREATE TABLE raw_data (
    identifier SERIAL PRIMARY KEY,
    company_id INT NOT NULL,
    observer_id INT,
    reference_id VARCHAR UNIQUE, -- external id - tweet id, app review id, youtube comment id etc
    parent_reference_id VARCHAR,
    processing_status SMALLINT DEFAULT 0,
    tags jsonb,
    raw_text TEXT,
    data jsonb,
    is_deleted boolean DEFAULT FALSE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT now(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT now(),
    observer_name varchar,
    observer_type varchar,
    entity_id int,
    entity_name varchar,
    regulated_entity_type varchar[],
    event_time timestamp with time zone

);
CREATE UNIQUE INDEX reference_id_idx ON raw_data (reference_id);


CREATE TABLE processed_data (
    identifier SERIAL PRIMARY KEY,
    company_id INT NOT NULL,
    raw_data_id INT NOT NULL,

    -- Extraction from Text
    service VARCHAR[],
    payment VARCHAR[],
    transfer VARCHAR[],
    account_type VARCHAR[],
    card VARCHAR[],
    identification VARCHAR[],
    security VARCHAR[],
    currency VARCHAR[],
    stock_market VARCHAR[],
    loan VARCHAR[],
    network VARCHAR[],

    -- Extraction from AI model
    emotion VARCHAR,
    fraud boolean,
    complaint boolean,
    harassment boolean,
    access boolean,
    delay boolean,
    interface boolean,
    charges boolean,

    -- Text Features
    text_length INT,
    text_lang VARCHAR,

    -- Entity Info
    entity_name VARCHAR,
    regulated_entity_type VARCHAR[],
    entity_country VARCHAR,
    entity_city VARCHAR,

    -- Observer Info
    observer_name VARCHAR,
    observer_type VARCHAR,

    -- To store some comment or un categories info
    remark VARCHAR,

    is_deleted boolean DEFAULT FALSE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT now(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT now(),
    event_time TIMESTAMP WITH TIME ZONE
);


CREATE TABLE issue_category (
	issue_type varchar NULL
);

--rollback DROP TABLE issue_category;
--rollback DROP TABLE raw_data;
--rollback DROP TABLE processed_data;
