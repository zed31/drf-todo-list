FROM python:3.6

ENV PYTHONUNBUFFERED 1

RUN mkdir /api/

WORKDIR /api/

ADD . /api/

RUN pip3 install -r requirements.txt
