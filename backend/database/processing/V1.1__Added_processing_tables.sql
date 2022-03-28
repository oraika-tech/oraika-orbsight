/* Migration script to create all tables */

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
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT now()
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
    fraud boolean DEFAULT FALSE,
    complaint boolean DEFAULT FALSE,
    harassment boolean DEFAULT FALSE,
    access boolean DEFAULT FALSE,
    delay boolean DEFAULT FALSE,
    interface boolean DEFAULT FALSE,
    charges boolean DEFAULT FALSE,

    -- Text Features
    text_length INT,
    text_lang VARCHAR,

    -- Entity Info
    entity_name VARCHAR,
    entity_type VARCHAR,
    entity_country VARCHAR,
    entity_city VARCHAR,

    -- Observer Info
    observer_name VARCHAR,
    observer_type VARCHAR,

    -- To store some comment or un categories info
    remark VARCHAR,

    is_deleted boolean DEFAULT FALSE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT now(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT now()
);

