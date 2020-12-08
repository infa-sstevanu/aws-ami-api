FROM python:3.8.6-alpine3.12

WORKDIR /app
COPY . /app

RUN pip install -r requirements.txt

RUN adduser -D apiuser
RUN chown -R apiuser /app

USER apiuser

ENV FLASK_APP ami_api

CMD gunicorn -w 2 -b 0.0.0.0:8080 "ami_api:create_app()"
