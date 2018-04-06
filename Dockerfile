FROM python:3.6-alpine3.7

MAINTAINER Open Knowledge International <sysadmin@okfn.org>

ENV LANG=en_US.UTF-8 \
    APP_DIR=/srv/app

RUN apk add --no-cache --virtual build-dependencies \
    build-base \
    linux-headers \
    python3-dev \
    libressl-dev \
    nodejs \
    nodejs-npm \
    readline-dev \
    git \
    curl \
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
    libressl \
    libpq \
    libjpeg-turbo \
    libpng \
    postgresql-client \
    make \
 && update-ca-certificates

WORKDIR ${APP_DIR}

ADD Makefile .
# Only required because the Makefile uses it to get the package name
ADD setup.py .

ADD requirements.txt .
RUN make install-backend

ADD package.json .
ADD package-lock.json .
RUN make install-frontend

COPY . ${APP_DIR}

RUN make frontend

EXPOSE 5000

CMD make server queue_mode=$QUEUE_MODE
