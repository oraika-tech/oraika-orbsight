$!/bin/zsh

set -x

for ssn in `redis-cli -p 63791 <<< 'scan 0 count 99 match ssn:*' | cut -f1 | grep ssn`; do
  echo $ssn
  redis-cli -p 63791 <<< 'hgetall '$ssn
done
