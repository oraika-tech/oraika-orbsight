CREATE TABLE user_auth (
	identifier SERIAL PRIMARY KEY,
	employee_id INT NOT NULL,
	login_name VARCHAR NOT NULL,
	hash_password VARCHAR NOT NULL,
	is_deleted boolean NULL DEFAULT false,
	created_at TIMESTAMP WITH TIME ZONE DEFAULT now(),
	updated_at TIMESTAMP WITH TIME ZONE DEFAULT now(),
	CONSTRAINT user_auth_user_id_key UNIQUE (login_name)
);