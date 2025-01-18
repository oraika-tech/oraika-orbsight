#!/bin/bash

DIR=$(dirname "$0")
source ${DIR}/../../../.env

set -e

if [ "$#" -lt 4 ]; then
    echo "Usage: $0 <tenant_name> <user_name> <user_email> <password>"
    exit 1
fi

TENANT_NAME=$1
USER_EMAIL=$2
USER_NAME=$3
PASSWORD=$4

# Convert tenant name to lowercase and remove spaces for code
TENANT_CODE=$(echo "$TENANT_NAME" | tr '[:upper:]' '[:lower:]' | tr ' ' '_')
DB_NAME="orb_tenant_${TENANT_CODE}"

# Function to hash password using bcrypt (requires python)
hash_password() {
    python3 -c "import bcrypt; print(bcrypt.hashpw('$1'.encode('utf-8'), bcrypt.gensalt(12)).decode('utf-8'))"
}

HASHED_PASSWORD=$(hash_password "$PASSWORD")

set -x

# Create database if not exists
psql postgresql://${ORBSIGHT_TENANT_USER}:${ORBSIGHT_TENANT_PASSWORD}@localhost:${DB_PORT}/postgres <<-EOSQL
    SELECT 'CREATE DATABASE ${DB_NAME} OWNER ${ORBSIGHT_TENANT_USER}'
    WHERE NOT EXISTS (SELECT 1 FROM pg_database WHERE datname = '${DB_NAME}')
    \gexec
EOSQL

# Grant privileges
# psql postgresql://${POSTGRES_USER}:${POSTGRES_PASSWORD}@localhost:${DB_PORT} <<-EOSQL
#     GRANT ALL PRIVILEGES ON DATABASE ${DB_NAME} TO ${ORBSIGHT_TENANT_USER};
# EOSQL

# Continue with tenant and user creation
psql postgresql://${ORBSIGHT_CORE_USER}:${ORBSIGHT_CORE_PASSWORD}@localhost:${DB_PORT}/orb_core <<-EOSQL
    DO \$\$
    DECLARE
        v_tenant_id uuid;
    BEGIN
        -- Insert or get tenant
        INSERT INTO tenant_master (name, code, type, is_enabled)
        VALUES ('$TENANT_NAME', '$TENANT_CODE', 1, TRUE)
        ON CONFLICT (code) DO UPDATE SET code = tenant_master.code
        RETURNING identifier INTO v_tenant_id;

        -- Insert tenant_global_config
        INSERT INTO tenant_global_config (tenant_id, config_key, config_value)
        VALUES (
            v_tenant_id,
            'connection_info',
            '{"db_engine_name": "postgresql", "db_name": "$DB_NAME"}'
        )
        ON CONFLICT (tenant_id, config_key) DO NOTHING;

        -- Insert user
        INSERT INTO user_master (tenant_ids, name, email, hash_password)
        VALUES (
            ARRAY[v_tenant_id],
            '$USER_NAME',
            '$USER_EMAIL',
            '$HASHED_PASSWORD'
        )
        ON CONFLICT (email) DO NOTHING;
    END
    \$\$;
EOSQL


