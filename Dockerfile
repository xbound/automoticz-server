FROM python:3.5-stretch

ENV C_FORCE_ROOT true
ENV FLASK_ENV development

COPY . /usr/src/app
WORKDIR /usr/src/app

RUN pip install -r requirements.txt

EXPOSE 8000
