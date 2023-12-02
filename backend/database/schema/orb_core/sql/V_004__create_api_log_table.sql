--liquibase formatted sql

--changeset girish:core_ddl_004

CREATE TABLE api_log_audit (
    identifier SERIAL PRIMARY KEY,
    --
    request_method TEXT NOT NULL,
    request_url TEXT NOT NULL,
    request_headers JSONB NOT NULL,
    request_body JSONB DEFAULT NULL,
    --
    processing_time INTEGER NOT NULL,
    --
    status_code INTEGER NOT NULL,
    response_headers JSONB NOT NULL,
    response_body JSONB DEFAULT NULL,
    --
	tenant_id UUID DEFAULT NULL,
	user_id UUID DEFAULT NULL,
	api_auth_id UUID DEFAULT NULL,
    --
	created_at TIMESTAMP WITH TIME ZONE DEFAULT now()
);

--rollback DROP TABLE api_log_audit;
