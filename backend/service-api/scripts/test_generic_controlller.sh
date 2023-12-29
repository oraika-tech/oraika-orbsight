#!/bin/bash

for table in entities observers categories taxonomies; do
  curl -X 'GET' \
    'http://api.oraika.local/api/v1/generic/'$table \
    -H 'accept: application/json' \
    -H 'origin: http://orb.oraika.local' \
    -H 'cookie: orb_web_session_id=2a00a33e-5f9d-4318-b24d-c2b083242839'
done

# This script will all combination of generic API. Once run check output manually.
