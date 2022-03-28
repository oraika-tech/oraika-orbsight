#!/usr/bin/env bash

DIR_PATH=$(dirname "$0")
FILE_NAME=$1

curl --location --request POST 'http://localhost:8080/v1/job/observer/ingestion' \
  --header 'Content-Type: application/json' \
  -d @"$DIR_PATH"/"$FILE_NAME"
