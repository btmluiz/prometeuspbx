#!/bin/bash

declare -a REQUIRED_ENVS=("PROMETEUSPBX_DATABASE_URL_FILE" "PROMETEUSPBX_SECRET_KEY_FILE" "PROMETEUSPBX_ALLOWED_HOSTS_FILE" "USE_X_FORWARDED_HOST_FILE" "ASTERISK_DATABASE_URL_FILE" "REDIS_URL_FILE")

for env in "${REQUIRED_ENVS[@]}"
do
  if [[ -z "${!env}" ]]; then
      printf "Container failed to start, pls pass -e %s=some-value\n" "$env"
      exit 1
  fi
done

python /app/manage.py migrate --noinput

exec "$@"
