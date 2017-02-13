FROM gliderlabs/alpine:3.4

MAINTAINER Paul Walsh <paulywalsh@gmail.com>

ENV LANG=en_US.UTF-8 \
    APP_DIR=/srv/app

COPY . ${APP_DIR}

WORKDIR ${APP_DIR}

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
    libxml2-dev \
    libxslt-dev \
    libstdc++ \
 && apk add --no-cache \
    python3 \
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
 && update-ca-certificates \
 && make install \
 && make install-frontend \
 && make frontend \
 && rm -rf node_modules \
 && apk del build-dependencies

EXPOSE 5000

CMD make server queue_mode=$QUEUE_MODE
