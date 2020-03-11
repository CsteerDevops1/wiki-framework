FROM python:3.7

COPY . /usr/src/app
WORKDIR /usr/src/app


RUN pip install --upgrade pip
RUN pip install -r requirements.txt
RUN mkdir music
RUN mkdir photos
RUN mkdir videos

ENTRYPOINT [ "python","main.py" ]