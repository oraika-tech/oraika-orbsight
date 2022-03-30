#!/usr/bin/env bash

REMOTE_PORT=8080
LOCAL_PORT=7070
SSH_PK_FILE=~/.ssh/id_rsa_aws
USER=ec2-user
HOST=ec2-54-77-212-91.eu-west-1.compute.amazonaws.com

ssh -N -L $LOCAL_PORT:localhost:$REMOTE_PORT -i $SSH_PK_FILE $USER@$HOST &
disown

echo Access Metabase: http://localhost:7070/
