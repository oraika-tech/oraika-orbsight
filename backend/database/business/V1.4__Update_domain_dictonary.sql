/* Removed old domain dictionary table and add new */

DROP TABLE domain_dictionary;

CREATE TABLE domain_dictionary (
    identifier SERIAL PRIMARY KEY,
    company_id INT NOT NULL,
    term VARCHAR NOT NULL,
    term_description VARCHAR,
    categories VARCHAR[],
    data jsonb,
    is_deleted boolean NULL DEFAULT false,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT now(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT now(),
    transaction_id SMALLINT,
    CONSTRAINT term_and_company UNIQUE (term, company_id)
);