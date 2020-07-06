FROM python:3.7

ENV SCHEMA_PATH schema.json
ENV FLASK_ENV production
ENV FLASK_HOST 0.0.0.0
ENV FLASK_PORT 5000
# ENV BASIC_AUTH_USERNAME username # should be set in .env file 
# ENV BASIC_AUTH_PASSWORD password
# ENV SECRET_KEY 123456879

# EXPOSE 5000-5000

ADD . /usr/src/coreService
WORKDIR /usr/src/coreService

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

ENTRYPOINT ["python","main.py"]