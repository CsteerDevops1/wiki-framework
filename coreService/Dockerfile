FROM python:3.7

ADD . /usr/src/app
WORKDIR /usr/src/app

ENV SCHEMA_PATH schema.json
ENV FLASK_ENV production
ENV FLASK_APP app.py
ENV FLASK_HOST 0.0.0.0
ENV FLASK_PORT 5000

EXPOSE 5000-5000

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

ENTRYPOINT ["python","app.py"]