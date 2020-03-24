FROM python:3.7

RUN pip install --upgrade pip
COPY requirements.txt /usr/src/app/requirements.txt
WORKDIR /usr/src/app

RUN pip install -r requirements.txt

COPY . /usr/src/app

ENTRYPOINT [ "python", "main.py" ]