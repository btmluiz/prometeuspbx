FROM btmluiz/asterisk:18-lts

COPY ../../conf/asterisk/ /etc/asterisk/

COPY ./docker-entrypoint.sh /docker-entrypoint.sh

ENTRYPOINT ["/bin/bash", "/docker-entrypoint.sh"]

CMD ["asterisk", "-mqf"]
