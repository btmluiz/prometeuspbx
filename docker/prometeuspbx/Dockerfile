FROM python:3.9

ENV TZ="America/Recife"

ENV PYTHONUNBUFFERED=1

ENV PROMETEUSPBX_DEBUG=0
ENV PROMETEUSPBX_DATABASE_URL=""
ENV PROMETEUSPBX_SECRET_KEY=""
ENV PROMETEUSPBX_ALLOWED_HOSTS="*"
ENV USE_X_FORWARDED_HOST=1
ENV ASTERISK_DATABASE_URL=""
ENV REDIS_URL=""

WORKDIR /app
COPY ./requirements.txt /app/

RUN pip install -r requirements.txt

COPY ./ /app/

COPY ../../conf/docker/prometeuspbx/docker-entrypoint.sh /docker-entrypoint.sh

ENTRYPOINT ["docker-entrypoint.sh"]
STOPSIGNAL SIGINT