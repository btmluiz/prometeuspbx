#!/bin/bash

# Start PrometeusPBX GUI Dependecies

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

# End PrometeusPBX GUI Dependecies

# Start Asterisk dependencies

declare -a REQUIRED_ENVS=("ASTERISK_DATABASE" "ASTERISK_DATABASE_USER" "ASTERISK_DATABASE_PASSWORD" "ASTERISK_DATABASE_PORT" "ASTERISK_DATABASE_HOST")

for env in "${REQUIRED_ENVS[@]}"
do
  if [[ -z "${!env}" ]]; then
      printf "Container failed to start, pls pass -e %s=some-value\n" "$env"
      exit 1
  fi
done

sed -s -E -i "s/dbhost=(.*)/dbhost=$ASTERISK_DATABASE_HOST/g" /etc/asterisk/*.conf
sed -s -E -i "s/dbport=(.*)/dbport=$ASTERISK_DATABASE_PORT/g" /etc/asterisk/*.conf
sed -s -E -i "s/dbuser=(.*)/dbuser=$ASTERISK_DATABASE_USER/g" /etc/asterisk/*.conf
sed -s -E -i "s/dbpass=(.*)/dbpass=$ASTERISK_DATABASE_PASSWORD/g" /etc/asterisk/*.conf
sed -s -E -i "s/dbname=(.*)/dbname=$ASTERISK_DATABASE/g" /etc/asterisk/*.conf

set -eo pipefail
shopt -s nullglob

if [[ "${1:0:1}" = '-' ]]; then
    set -- asterisk "$@"
fi

chown -R asterisk:asterisk /var/lib/asterisk/db
chown -R asterisk:asterisk /var/log/asterisk
chown -R asterisk:asterisk /var/spool/asterisk

if [[ "${1}" = "asterisk" ]]; then
    if [[ "$(id -u)" = "0" ]]; then
        exec gosu asterisk "$@"
    fi

    exec asterisk "$@"
fi

if [[ "$PROMETEUSPBX_DEBUG" ]]; then
    asterisk -fT &
    python manage.py runserver 0.0.0.0:8000
else
    gunicorn --bind :8000 PrometeusPBX.wsgi:application --daemon --capture-output --log-file /var/log/prometeuspbx/access.log
    asterisk -fT
fi
