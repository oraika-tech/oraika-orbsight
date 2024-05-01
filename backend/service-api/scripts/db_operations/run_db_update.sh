#!/bin/bash

# SSH Tunnel Check (idempotent)
if ! nc -zv localhost 5433 &>/dev/null; then  # Use netcat (nc) to check port availability
    ssh -fNL 5433:prod-orbsight.cu4iby7ba2we.eu-west-1.rds.amazonaws.com:5432 -i ~/.ssh/id_rsa_aws ec2-user@ec2-34-255-28-113.eu-west-1.compute.amazonaws.com
    echo "Connected remote DB"
fi

# Virtual Environment Check (idempotent)
if [[ -z $(python -c "import sys; print('oraika-env' in sys.modules)") ]]; then 
    source /Users/girish/programs/oraika-env/bin/activate
    echo "Sourced python env"
fi

# Environment Sourcing Check (idempotent)
if [[ -z $CORE_DB_USER ]]; then
    source ~/.oraika/db_operation.env
    echo "Sourced DB env"
fi

python db_update_operation.py 
echo "Done!"
