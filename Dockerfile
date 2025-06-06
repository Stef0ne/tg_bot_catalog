FROM python:3.12-alpine

WORKDIR /usr/src/app

COPY requirements.txt ./

RUN pip install -r requirements.txt
RUN apk add --no-cache bash

COPY . .