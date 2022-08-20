#!/bin/bash

declare -a REQUIRED_ENVS=("PROMETEUSPBX_DATABASE_URL" "PROMETEUSPBX_SECRET_KEY" "PROMETEUSPBX_ALLOWED_HOSTS" "USE_X_FORWARDED_HOST" "ASTERISK_DATABASE_URL" "REDIS_URL")

for env in "${REQUIRED_ENVS[@]}"
do
  if [[ -z "${!env}" ]]; then
      printf "Container failed to start, pls pass -e %s=some-value\n" "$env"
      exit 1
  fi
done

python /app/manage.py migrate --noinput

exec "$@"
