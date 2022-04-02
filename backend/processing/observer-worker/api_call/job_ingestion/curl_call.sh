#!/usr/bin/env bash

DIR_PATH=$(dirname "$0")
FILE_NAME=$1

case $FILE_NAME in
android)
  FILE_NAME=android_job.json
  ;;
ios)
  FILE_NAME=ios_job.json
  ;;
twitter)
  FILE_NAME=twitter_job.json
  ;;
esac

curl --location --request POST 'http://localhost:8080/v1/job/observer/ingestion' \
  --header 'Content-Type: application/json' \
  -d @"$DIR_PATH"/"$FILE_NAME"
