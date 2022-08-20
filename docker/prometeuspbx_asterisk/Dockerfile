FROM btmluiz/asterisk:18-lts

COPY ../../conf/asterisk/ /etc/asterisk/

COPY ../../conf/docker/prometeuspbx_asterisk/docker-entrypoint.sh /docker-entrypoint.sh

RUN chmod +x /docker-entrypoint.sh
ENTRYPOINT ["/docker-entrypoint.sh"]

CMD ["asterisk", "-mqf"]
