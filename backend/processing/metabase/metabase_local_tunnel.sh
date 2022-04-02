#!/usr/bin/env bash

REMOTE_PORT=${METABASE_REMOTE_PORT:-80}
HOST=${METABASE_HOST:-ec2-34-253-228-40.eu-west-1.compute.amazonaws.com}

LOCAL_PORT=${LOCAL_PORT:-7070}
SSH_PK_FILE=${SSH_PK_FILE:-~/.ssh/id_rsa_aws}
USER=ec2-user

ssh -N -L $LOCAL_PORT:localhost:"$REMOTE_PORT" -i $SSH_PK_FILE $USER@"$HOST" &
disown

echo Access Metabase: http://localhost:7070/
