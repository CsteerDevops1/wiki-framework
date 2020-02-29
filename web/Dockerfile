FROM python:3.7

ADD . /usr/src/app
WORKDIR /usr/src/app

RUN apt update
RUN apt install -y python3-flask

RUN pip install --upgrade pip
RUN pip install -r requirements.txt



ENV SCHEMA_PATH schema.json
ENV FLASK_ENV production
ENV FLASK_APP run.py
ENV FLASK_HOST 0.0.0.0
ENV FLASK_PORT 8000
EXPOSE 8000-8000
ENTRYPOINT flask run --host 0.0.0.0 --port 8000
