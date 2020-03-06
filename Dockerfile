FROM python:3.6.9-alpine

WORKDIR /data/workspace/apiexample

COPY src/* /data/workspace/apiexample/

ENV PYTHONPATH /data/workspace

RUN apk --update add mysql-client mysql py-mysqldb mariadb-dev build-base

RUN pip install --no-cache-dir -r requirements.txt
RUN pip install waitress

EXPOSE 5000

CMD waitress-serve --port=5000 --host=0.0.0.0 --call app:get_app