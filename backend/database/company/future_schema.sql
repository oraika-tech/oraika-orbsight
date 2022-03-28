
CREATE TABLE organization (
    identifier SERIAL PRIMARY KEY,
    name VARCHAR NOT NULL,
    is_enabled boolean DEFAULT TRUE,
    is_deleted boolean DEFAULT FALSE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT now(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT now()
)

CREATE TABLE account (
    identifier SERIAL PRIMARY KEY,
    name VARCHAR NOT NULL,
    is_enabled boolean DEFAULT TRUE,
    is_deleted boolean DEFAULT FALSE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT now(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT now()
);

