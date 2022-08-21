#!/bin/bash

declare -a REQUIRED_ENVS=("PROMETEUSPBX_DATABASE_URL" "PROMETEUSPBX_SECRET_KEY" "PROMETEUSPBX_ALLOWED_HOSTS" "USE_X_FORWARDED_HOST" "ASTERISK_DATABASE_URL" "REDIS_URL")
declare -a OPTIONAL_ENVS=("PROMETEUSPBX_ALLOWED_HOSTS" "PROMETEUSPBX_DEBUG")

touch .env

for env in "${REQUIRED_ENVS[@]}"
do
  if [[ -z "${!env}" ]]; then
      printf "Container failed to start, pls pass -e %s=some-value\n" "$env"
      exit 1
  else
    echo "$env=${!env}" >> .env
  fi
done

for env in "${OPTIONAL_ENVS[@]}"
do
  if [[ -z "${!env}" ]]; then
      continue # skip if env is not set
  else
    echo "$env=${!env}" >> .env
  fi
done

python /app/manage.py migrate --noinput
python /app/manage.py migrate --noinput --database=asterisk

exec "$@"
