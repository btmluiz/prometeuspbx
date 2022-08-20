FROM python:3.9

ENV TZ="America/Recife"

ENV PYTHONUNBUFFERED=1

ENV PROMETEUSPBX_DEBUG_FILE=0
ENV PROMETEUSPBX_DATABASE_URL_FILE=""
ENV PROMETEUSPBX_SECRET_KEY_FILE=""
ENV PROMETEUSPBX_ALLOWED_HOSTS_FILE="*"
ENV USE_X_FORWARDED_HOST_FILE=1
ENV ASTERISK_DATABASE_URL_FILE=""
ENV REDIS_URL_FILE=""

WORKDIR /app
COPY ./requirements.txt /app/

RUN pip install -r requirements.txt

COPY ./ /app/

COPY ../../conf/docker/prometeuspbx/docker-entrypoint.sh /docker-entrypoint.sh

RUN chmod +x /docker-entrypoint.sh
ENTRYPOINT ["/docker-entrypoint.sh"]
STOPSIGNAL SIGINT

CMD ["gunicorn", "--bind", ":8000", "PrometeusPBX.wsgi:application"]