/* Migration script to create all tables */


CREATE TABLE company (
    id SERIAL PRIMARY KEY,
    name VARCHAR NOT NULL,
    type SMALLINT NOT NULL, -- CORPORATE | GOV | INDIVIDUAL
    is_enabled boolean DEFAULT TRUE,
    is_deleted boolean DEFAULT FALSE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT now(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT now()
);


CREATE TABLE employee (
    id SERIAL PRIMARY KEY,
    name VARCHAR NOT NULL,
    email VARCHAR,
    company_id INT, --
    role_ids INT[],
    is_email_verified BOOLEAN,
    is_enabled boolean DEFAULT TRUE,
    is_deleted boolean DEFAULT FALSE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT now(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT now()
);

CREATE TABLE role (
    id SERIAL PRIMARY KEY,
    name VARCHAR NOT NULL,
    company_id INT, -- NULL for global role or company_id for company specific role
    is_enabled boolean DEFAULT TRUE,
    is_deleted boolean DEFAULT FALSE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT now(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT now()
);

CREATE TABLE role_permission (
    id SERIAL PRIMARY KEY,
    role_id INT NOT NULL,
    permission VARCHAR NOT NULL,
    is_enabled boolean DEFAULT TRUE,
    is_deleted boolean DEFAULT FALSE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT now(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT now()
);

