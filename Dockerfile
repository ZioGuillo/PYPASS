FROM ubuntu:latest
MAINTAINER PABLO CISNEROS "pcisnerp@gmail.com"
RUN apt-get update \
  && apt-get install -y python3-pip python3-dev libsasl2-dev python-dev libldap2-dev libssl-dev libsnmp-dev apt-utils \
  && cd /usr/local/bin \
  && ln -s /usr/bin/python3 python \
  && pip3 install --upgrade pip

COPY    . /app

WORKDIR /app/app

RUN pip install -r requirements.txt

EXPOSE 5000

ENTRYPOINT  ["python3"]

CMD ["app.py"]
