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
    processed_text TEXT NOT NULL,
    entity_type VARCHAR,
    category VARCHAR,
    payment VARCHAR,
    feature VARCHAR,
    account_type VARCHAR,
    issue_type VARCHAR,
    sentiment VARCHAR,
    emotion VARCHAR,
    observer VARCHAR,
    channel VARCHAR,
    app_id VARCHAR,
    region VARCHAR,
    city VARCHAR,
    state VARCHAR,
    country VARCHAR,
    is_deleted boolean DEFAULT FALSE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT now(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT now()
);

