#!/usr/bin/env bash 

set -x

docker run -ti --rm alpine/psql:17.2 $@

