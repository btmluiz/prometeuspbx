FROM postgres:14

ENV ASTERISK_USER asterisk
ENV ASTERISK_DB asterisk
ENV PROMETEUSPBX_USER prometeuspbx
ENV PROMETEUSPBX_DB prometeuspbx

COPY create-db.sh /docker-entrypoint-initdb.d/

RUN chmod +x /docker-entrypoint-initdb.d/create-db.sh

EXPOSE 5432