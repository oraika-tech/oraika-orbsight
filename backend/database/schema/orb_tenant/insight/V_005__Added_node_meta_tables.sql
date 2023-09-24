--liquibase formatted sql

--changeset girish:insight_ddl_005

CREATE TABLE workflow_node_meta (
    identifier SERIAL PRIMARY KEY,
    data_id INT NOT NULL,
    status VARCHAR(50) NOT NULL,
    error_message TEXT,
    additional_data JSONB,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT now(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT now()
);

--rollback DROP TABLE workflow_node_meta;
