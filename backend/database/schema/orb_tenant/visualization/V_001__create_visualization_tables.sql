--liquibase formatted sql

--changeset girish:viz_ddl_001

CREATE TABLE viz_dashboard (
    identifier UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
    ----
    frontend_keys VARCHAR[] NOT NULL,
    title VARCHAR,
    component_layout JSONB NOT NULL,
    ----
    is_enabled boolean DEFAULT TRUE,
    is_deleted boolean DEFAULT FALSE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT now(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT now(),
    transaction_id SMALLINT
);

CREATE TABLE viz_chart (
    identifier UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
    ----
    data_source_type VARCHAR NOT NULL,
    data_source_series JSONB NOT NULL DEFAULT '{}',
    chart_type VARCHAR NOT NULL,
    chart_config JSONB NOT NULL DEFAULT '{}',
    data_field_mapping JSONB NOT NULL DEFAULT '{}',
    ----
    is_enabled boolean DEFAULT TRUE,
    is_deleted boolean NULL DEFAULT FALSE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT now(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT now(),
    transaction_id SMALLINT
);

--rollback DROP TABLE viz_chart;
--rollback DROP TABLE viz_dashboard;
