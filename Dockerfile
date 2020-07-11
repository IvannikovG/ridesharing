FROM python:3.7-alpine

RUN apk update && apk add postgresql-dev gcc libc-dev make git libffi-dev openssl-dev python3-dev libxml2-dev libxslt-dev

RUN adduser -D ridesharing

WORKDIR /home/ridesharing

COPY requirements.txt requirements.txt
RUN python3 -m venv venv
RUN venv/bin/pip3 install -r requirements.txt
RUN venv/bin/pip3 install gunicorn

COPY app app
COPY migrations migrations
COPY ridesharing.py config.py boot.sh ./
RUN chmod +x boot.sh

ENV FLASK_APP ridesharing.py

RUN chown -R ridesharing:ridesharing ./
USER ridesharing

EXPOSE 5000
ENTRYPOINT ["./boot.sh"]
