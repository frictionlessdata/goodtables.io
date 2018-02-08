FROM python:3.5-alpine

MAINTAINER Open Knowledge International <sysadmin@okfn.org>

ENV LANG=en_US.UTF-8 \
    APP_DIR=/srv/app

RUN apk add --no-cache --virtual build-dependencies \
    build-base \
    linux-headers \
    python3-dev \
    openssl-dev \
    readline-dev \
    git \
    curl \
    nodejs \
    postgresql-dev \
    libpng-dev \
    libjpeg-turbo-dev \
    libffi-dev \
 && apk add --no-cache --update \
    libstdc++ \
    libxml2-dev \
    libxslt-dev \
    bzip2 \
    bash \
    gettext \
    ca-certificates \
    openssl \
    libpq \
    libjpeg-turbo \
    libpng \
    postgresql-client \
    make \
 && update-ca-certificates

COPY . ${APP_DIR}

WORKDIR ${APP_DIR}

RUN make install \
  && make frontend \
  && rm -rf node_modules \
  && apk del build-dependencies

EXPOSE 5000

CMD make server queue_mode=$QUEUE_MODE
