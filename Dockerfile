FROM python:3.8.6-alpine3.12

WORKDIR /app
COPY . /app

RUN pip install -r requirements.txt

RUN adduser -D ami-api
RUN chown -R ami-api /app

USER ami-api

ENV FLASK_APP ami_api
ENV FLASK_ENV development

CMD flask run --host=0.0.0.0
