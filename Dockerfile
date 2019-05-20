FROM node:8-alpine as builder
MAINTAINER Open Knowledge Foundation <sysadmin@okfn.org>
WORKDIR /app

RUN apk add --no-cache \
    build-base \
    git \
    libpng-dev \
    libjpeg-turbo-dev \
    libffi-dev \
    bash \
    make

COPY package.json .
COPY package-lock.json .

RUN npm install

COPY setup.py .
COPY Makefile .
COPY webpack.config.js .

COPY . .
RUN make frontend

FROM python:3.5-alpine

MAINTAINER Open Knowledge Foundation <sysadmin@okfn.org>

ENV LANG=en_US.UTF-8 \
    APP_DIR=/srv/app

WORKDIR ${APP_DIR}

RUN apk add --no-cache --virtual build-dependencies \
    build-base \
    linux-headers \
    python3-dev \
    libressl-dev \
    readline-dev \
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

COPY requirements.txt .
COPY Makefile .

RUN make install-backend \
  && apk del build-dependencies

COPY --from=builder /app/public ./public
COPY . .

EXPOSE 5000

CMD make server queue_mode=$QUEUE_MODE
