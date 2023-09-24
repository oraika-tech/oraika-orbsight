#!/usr/bin/env bash

DIR_PATH=$(dirname "$0")
FILE_NAME=$1

case $FILE_NAME in
android)
  FILE_NAME=android_event.json
  ;;
ios)
  FILE_NAME=ios_event.json
  ;;
twitter)
  FILE_NAME=twitter_event.json
  ;;
esac

curl --location --request POST 'http://localhost:8080/v1/job/analyzer/ingestion' \
  --header 'Content-Type: application/json' \
  -d @"$DIR_PATH"/"$FILE_NAME"
