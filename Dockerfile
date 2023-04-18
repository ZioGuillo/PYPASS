FROM ubuntu:22.04

WORKDIR /app

RUN apt-get update \
  && apt-get install -y python3-pip python3-dev libsasl2-dev libldap2-dev libssl-dev libsnmp-dev apt-utils iputils-ping \
  && cd /usr/local/bin \
  && ln -s /usr/bin/python3 python \
  && pip3 install --upgrade pip

COPY ./app /app

RUN pip install -r requirements.txt
