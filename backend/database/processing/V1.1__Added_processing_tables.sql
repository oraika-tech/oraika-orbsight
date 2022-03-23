/* Migration script to create all tables */

CREATE TABLE raw_data (
    id SERIAL PRIMARY KEY,
    company_id INT NOT NULL,
    observer_id INT,
    reference_id VARCHAR, -- external id - tweet id, app review id, youtube comment id etc
    parent_reference_id VARCHAR, -- external id - tweet id, app review id, youtube comment id etc
    processing_status SMALLINT,
    tags VARCHAR[],
    raw_text TEXT,
    data jsonb,
    is_deleted boolean DEFAULT FALSE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT now(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT now()
);

CREATE TABLE processed_data (
    id SERIAL PRIMARY KEY,
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

