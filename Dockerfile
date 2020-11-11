FROM python:3.8-slim
MAINTAINER bpereto

# set environment variables
ENV PYTHONDONTWRITEBYTE 1
ENV PYTHONUNBUFFERED 1
ENV DEBIAN_FRONTEND noninteractive

RUN apt-get update && apt-get install -y libmariadbclient-dev mariadb-client gcc && rm -rf /var/lib/apt/lists/*

RUN mkdir /app /staticfiles && groupadd -g 1000 upd && \
    useradd -rm -u 1000 -g 1000 upd && chown -R upd:upd /app /staticfiles /media
WORKDIR /app
COPY requirements.txt /app/

RUN pip3 install --no-cache -r requirements.txt

# install uwsgi now because it takes a little while
RUN pip3 install --no-cache uwsgi

COPY src /app/
COPY scripts/init.sh /
COPY uwsgi.ini /

VOLUME ["/staticfiles"]

USER upd

ENTRYPOINT ["/init.sh"]
