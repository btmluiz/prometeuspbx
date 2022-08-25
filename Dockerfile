FROM ubuntu:focal as build

# Build asterisk dependencies

RUN     sed -i -e 's:# deb-src :deb-src :' /etc/apt/sources.list && \
        apt-get update && \
        export DEBIAN_FRONTEND=noninteractive DEBCONF_NONINTERACTIVE_SEEN=true && \
        apt-get -y install debconf-utils wget && \
        echo "libvpb1 libvpb1/countrycode string 1"  | debconf-set-selections && \
        echo "tzdata tzdata/Areas select Etc"        | debconf-set-selections && \
        echo "tzdata tzdata/Zones/Etc select UTC"    | debconf-set-selections && \
        echo "Etc/UTC" > /etc/timezone && \
        apt-get -y build-dep asterisk

ARG asterisk_version=18.5.0

RUN     wget -O asterisk.tar.gz http://downloads.asterisk.org/pub/telephony/asterisk/releases/asterisk-${asterisk_version}.tar.gz && \
        tar xzf asterisk.tar.gz
RUN     cd asterisk-${asterisk_version} && \
        ./configure --with-dahdi=no --with-pri=no --with-pjproject-bundled \
        && make menuselect.makeopts \
        && menuselect/menuselect --disable BUILD_NATIVE menuselect.makeopts \
        && make ASTDBDIR=/var/lib/asterisk/db -j$(grep -c ^processor /proc/cpuinfo) && make install

FROM ubuntu:focal as python-build

ENV PATH /usr/local/bin:$PATH

# http://bugs.python.org/issue19846
# > At the moment, setting "LANG=C" on a Linux system *fundamentally breaks Python 3*, and that's not OK.
ENV LANG C.UTF-8

# runtime dependencies
RUN set -eux; \
	apt-get update; \
    export DEBIAN_FRONTEND=noninteractive DEBCONF_NONINTERACTIVE_SEEN=true ;\
    apt-get install build-essential libssl-dev libffi-dev libpq-dev wget -y ;\
	apt-get install -y --no-install-recommends \
		libbluetooth-dev \
		tk-dev \
		uuid-dev \
	; \
	rm -rf /var/lib/apt/lists/*

ENV GPG_KEY E3FF2839C048B25C084DEBE9B26995E310250568
ENV PYTHON_VERSION 3.9.13

RUN set -eux; \
	\
	wget -O python.tar.xz "https://www.python.org/ftp/python/${PYTHON_VERSION%%[a-z]*}/Python-$PYTHON_VERSION.tar.xz"; \
	wget -O python.tar.xz.asc "https://www.python.org/ftp/python/${PYTHON_VERSION%%[a-z]*}/Python-$PYTHON_VERSION.tar.xz.asc"; \
	GNUPGHOME="$(mktemp -d)"; export GNUPGHOME; \
	gpg --batch --keyserver hkps://keys.openpgp.org --recv-keys "$GPG_KEY"; \
	gpg --batch --verify python.tar.xz.asc python.tar.xz; \
	command -v gpgconf > /dev/null && gpgconf --kill all || :; \
	rm -rf "$GNUPGHOME" python.tar.xz.asc; \
	mkdir -p /usr/src/python; \
	tar --extract --directory /usr/src/python --strip-components=1 --file python.tar.xz; \
	rm python.tar.xz; \
	\
	cd /usr/src/python; \
	gnuArch="$(dpkg-architecture --query DEB_BUILD_GNU_TYPE)"; \
	./configure \
		--build="$gnuArch" \
		--enable-loadable-sqlite-extensions \
		--enable-optimizations \
		--enable-option-checking=fatal \
		--enable-shared \
		--with-system-expat \
		--without-ensurepip \
	; \
	nproc="$(nproc)"; \
	make -j "$nproc" \
	; \
	make install; \
	\
# enable GDB to load debugging data: https://github.com/docker-library/python/pull/701
	bin="$(readlink -ve /usr/local/bin/python3)"; \
	dir="$(dirname "$bin")"; \
	mkdir -p "/usr/share/gdb/auto-load/$dir"; \
	cp -vL Tools/gdb/libpython.py "/usr/share/gdb/auto-load/$bin-gdb.py"; \
	\
	cd /; \
	rm -rf /usr/src/python; \
	\
	find /usr/local -depth \
		\( \
			\( -type d -a \( -name test -o -name tests -o -name idle_test \) \) \
			-o \( -type f -a \( -name '*.pyc' -o -name '*.pyo' -o -name 'libpython*.a' \) \) \
		\) -exec rm -rf '{}' + \
	; \
	\
	ldconfig; \
	\
	python3 --version

# make some useful symlinks that are expected to exist ("/usr/local/bin/python" and friends)
RUN set -eux; \
	for src in idle3 pydoc3 python3 python3-config; do \
		dst="$(echo "$src" | tr -d 3)"; \
		[ -s "/usr/local/bin/$src" ]; \
		[ ! -e "/usr/local/bin/$dst" ]; \
		ln -svT "$src" "/usr/local/bin/$dst"; \
	done

# if this is called "PIP_VERSION", pip explodes with "ValueError: invalid truth value '<VERSION>'"
ENV PYTHON_PIP_VERSION 22.0.4
# https://github.com/docker-library/python/issues/365
ENV PYTHON_SETUPTOOLS_VERSION 58.1.0
# https://github.com/pypa/get-pip
ENV PYTHON_GET_PIP_URL https://github.com/pypa/get-pip/raw/5eaac1050023df1f5c98b173b248c260023f2278/public/get-pip.py
ENV PYTHON_GET_PIP_SHA256 5aefe6ade911d997af080b315ebcb7f882212d070465df544e1175ac2be519b4

RUN set -eux; \
	\
	wget -O get-pip.py "$PYTHON_GET_PIP_URL"; \
	echo "$PYTHON_GET_PIP_SHA256 *get-pip.py" | sha256sum -c -; \
	\
	export PYTHONDONTWRITEBYTECODE=1; \
	\
	python get-pip.py \
		--disable-pip-version-check \
		--no-cache-dir \
		--no-compile \
		"pip==$PYTHON_PIP_VERSION" \
		"setuptools==$PYTHON_SETUPTOOLS_VERSION" \
	; \
	rm -f get-pip.py; \
	\
	pip --version

CMD ["python3"]

FROM python-build
MAINTAINER Luiz Braga <contato@luizbraga.dev>

ENV TZ="America/Recife"

ENV PYTHONUNBUFFERED=1

ENV PROMETEUSPBX_DEBUG=0
ENV PROMETEUSPBX_DATABASE_URL=""
ENV PROMETEUSPBX_SECRET_KEY=""
ENV PROMETEUSPBX_ALLOWED_HOSTS="*"
ENV USE_X_FORWARDED_HOST=1
ENV ASTERISK_DATABASE_URL=""
ENV REDIS_URL=""
ENV PROMETEUSPBX_CSRF_TRUSTED_ORIGINS=""
ENV PROMETEUSPBX_PORT=8000

RUN     apt-get update && \
        apt-get -y install debconf-utils && \
        echo "libvpb1 libvpb1/countrycode string 1"  | debconf-set-selections && \
        echo "tzdata tzdata/Areas select Etc"        | debconf-set-selections && \
        echo "tzdata tzdata/Zones/Etc select UTC"    | debconf-set-selections && \
        echo "Etc/UTC" > /etc/timezone && \
        export DEBIAN_FRONTEND=noninteractive DEBCONF_NONINTERACTIVE_SEEN=true && \
        apt-get -y install gosu libcap2 libedit2 libjansson4 libpopt0 libsqlite3-0 libssl1.1 \
                libsystemd0 liburiparser1 libuuid1 libxml2 libxslt1.1 libjack0 libresample1 \
                libodbc1 libpq5 libsdl1.2debian libcurl4 libgsm1 liblua5.1-0 libgmime-3.0-0 \
                libical3 libiksemel3 libneon27-gnutls libportaudio2 libpri1.4 libradcli4 \
                libspandsp2 libspeex1 libspeexdsp1 libsqlite0 libsrtp2-1 libss7-2.0 libsybdb5 \
                libtonezone2.0 libvorbisfile3 && \
        apt-get clean

# Copy asterisk dependecies
COPY --from=build   /var/spool/asterisk /var/spool/asterisk
COPY --from=build   /var/lib/asterisk   /var/lib/asterisk
COPY --from=build   /usr/lib/asterisk   /usr/lib/asterisk
COPY --from=build   /usr/lib/libasteriskpj.so \
                    /usr/lib/libasteriskssl.so \
                    /usr/lib/
COPY --from=build   /usr/sbin/astcanary \
                    /usr/sbin/astdb2bdb \
                    /usr/sbin/astdb2sqlite3 \
                    /usr/sbin/asterisk \
                    /usr/sbin/astgenkey \
                    /usr/sbin/astversion \
                    /usr/sbin/autosupport \
                    /usr/sbin/rasterisk \
                    /usr/sbin/safe_asterisk \
                    /usr/sbin/

RUN     groupadd -g 999 asterisk && useradd -s /bin/false -d /var/lib/asterisk -g asterisk -u 999 asterisk && \
        mkdir -p /var/run/asterisk /var/log/asterisk && \
        chown -R asterisk:asterisk /var/lib/asterisk && \
        chown -R asterisk:asterisk /var/spool/asterisk && \
        chown -R asterisk:asterisk /var/log/asterisk && \
        chown asterisk:asterisk /var/run/asterisk && \
        ldconfig

COPY ./conf/asterisk/ /etc/asterisk/

# End copy asterisk dependecies

## Install PrometeusPBX dependecies
WORKDIR /app

RUN pip install poetry

COPY poetry.lock pyproject.toml /app/

RUN poetry config virtualenvs.create false
RUN poetry install --no-interaction

COPY docker-entrypoint.sh /docker-entrypoint.sh
COPY ./ /app/


RUN mkdir -p /var/log/prometeuspbx
RUN chmod +x /docker-entrypoint.sh

VOLUME  [ "/var/lib/asterisk/db", "/var/spool/asterisk/voicemail", "/var/spool/asterisk/monitor", "/etc/asterisk/custom" ]
ENTRYPOINT ["/docker-entrypoint.sh"]
STOPSIGNAL SIGINT
