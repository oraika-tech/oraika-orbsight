--liquibase formatted sql

--changeset girish:insight_ddl_001

CREATE TABLE insight_raw_data (
    identifier SERIAL PRIMARY KEY,
    observer_id UUID NOT NULL,
    reference_id VARCHAR UNIQUE, -- external id - tweet id, app review id, youtube comment id etc
    parent_reference_id VARCHAR,
    raw_text TEXT,
    unstructured_data jsonb,
    event_time timestamp with time zone,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT now(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT now(),
    is_deleted boolean DEFAULT FALSE
);
CREATE UNIQUE INDEX raw_data_reference_id_idx ON insight_raw_data ( reference_id );
CREATE INDEX raw_data_event_time_idx ON insight_raw_data USING brin( event_time );
CREATE INDEX raw_data_observer_id_idx ON insight_raw_data ( observer_id );


CREATE TABLE insight_processed_data (
    identifier SERIAL PRIMARY KEY,
    raw_data_id INT NOT NULL,

    -- Extraction from Text
    taxonomy_tags VARCHAR[],
    taxonomy_terms VARCHAR[],

    -- Extraction from AI model
    emotion VARCHAR,
    categories VARCHAR[],

    -- Text Features
    text_length INT,
    text_lang VARCHAR,

    -- To store some comment or un categories info
    remark VARCHAR,

    created_at TIMESTAMP WITH TIME ZONE DEFAULT now(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT now(),
    is_deleted boolean DEFAULT FALSE
);
CREATE INDEX processed_data_text_lang_idx ON insight_processed_data USING hash( text_lang );
CREATE INDEX processed_data_emotion_idx ON insight_processed_data ( emotion ) where emotion is not null;
CREATE INDEX processed_data_raw_data_id_idx ON insight_processed_data ( raw_data_id desc );

--rollback DROP TABLE insight_raw_data;
--rollback DROP TABLE insight_processed_data;
