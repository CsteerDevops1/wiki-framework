FROM python:3.7

ADD . /usr/src/app
WORKDIR /usr/src/app

ENV API_KEY trnsl.1.1.20200309T121046Z.10fd25429d4264e1.1b1d8883b0e564975a110cb11b558d5d1e1aa68b
ENV API_ADDRESS http://127.0.0.1:5000/api/wiki

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

ENTRYPOINT ["python","app.py"]
