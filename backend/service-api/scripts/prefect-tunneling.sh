#!/bin/bash

# Find remote EC2 host machine port for prefect server
PORT=$(ssh -i ~/.ssh/id_rsa_aws ec2-user@ec2-34-255-28-113.eu-west-1.compute.amazonaws.com \
    'ssh 10.0.1.102 docker ps | grep service-api | head -1' | grep -o '0.0.0.0:\d\+->4200' | grep -o '\d\{5\}')

if [[ -z $PORT ]]; then
  echo "Port not found, check manually"
  exit 1
else
  echo "Received port ${PORT}"
fi

# Find the PID of the process using port 4200
PID=$(lsof -i :4200 | awk 'NR>1 {print $2}' | uniq)

# Kill the process
if [ ! -z "$PID" ]; then
  kill -9 $PID
  echo "Killed process with PID: $PID"
else
  echo "No process found using port 4200"
fi

ssh -fNL 4200:10.0.1.102:$PORT -i ~/.ssh/id_rsa_aws ec2-user@ec2-34-255-28-113.eu-west-1.compute.amazonaws.com                                                                  [0]
if [[ $? == 0 ]]; then
  echo "Tunneling Success"
else
  echo "Tunneling Failed"
fi
