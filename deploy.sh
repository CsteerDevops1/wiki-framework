#!/bin/bash

#---------------------------- PRE-REQUIREMENTS ----------------------------
if ! [ -x "$(command -v git)" ]; then
  echo 'Error: git is not installed.' >&2
  echo 'Installing git'
  sudo apt install git-all -y
fi

if ! [ -x "$(command -v docker)" ]; then
  echo 'Error: docker is not installed.' >&2
  echo 'Installing docker'
  sudo apt-get update
  sudo apt-get install \
    apt-transport-https \
    ca-certificates \
    curl \
    gnupg-agent \
    software-properties-common -y
  curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
  sudo add-apt-repository \
   "deb [arch=amd64] https://download.docker.com/linux/ubuntu \
   $(lsb_release -cs) \
   stable"
  sudo apt-get update
  sudo apt-get install docker-ce docker-ce-cli containerd.io -y

  if ! getent group docker > /dev/null 2>&1; then
    sudo groupadd docker
  fi
  if ! groups | grep docker &> /dev/null; then
    sudo usermod -aG docker $USER
    # newgrp docker # logins in new console => BAD
  fi

fi

if ! [ -f "docker-compose" ]; then
  echo 'Error: docker-compose doesnt exists' >&2
  wget "https://github.com/docker/compose/releases/download/1.25.4/docker-compose-$(uname -s)-$(uname -m)" \
    -O ./docker-compose
  chmod +x ./docker-compose
fi

if [ "$1" != "" ]; then
    PROJECT_DIR="$1"
else
    PROJECT_DIR="$(pwd)"
fi

echo "Project folder is set to $PROJECT_DIR"
if ! [ -d "$PROJECT_DIR" ]; then
    echo "Creating project folder"
    mkdir "$PROJECT_DIR"
fi

#---------------------------- CLONING GIT ----------------------------

git clone https://github.com/CsteerDevops1/wiki-framework "$PROJECT_DIR"
cd "$PROJECT_DIR"
git checkout develop
cd ../

#---------------------------- STARTING CORE SERVICE ----------------------------
if [ -d "$PROJECT_DIR/coreService/data/db" ]; then
    :
else
    echo "Creating $PROJECT_DIR/coreService/data/db folder"
    mkdir $PROJECT_DIR/coreService/data
    mkdir $PROJECT_DIR/coreService/data/db
fi

echo "Launching docker-compose"

# used to config user for mongodb
export UID=${UID}
export GID=${GID}

# ./docker-compose -f $PROJECT_DIR/coreService/docker-compose.yml up --build -d
# don't use sudo if it's unnecessary
if ! groups | grep docker &> /dev/null; then
 sudo ./docker-compose -f ./docker-compose.yml up --build -d
else
 docker-compose -f ./docker-compose.yml up --build -d
fi

#---------------------------- STARTING WEB SERVICE ----------------------------
if ! [ -x "$(command -v npm)" ]; then
  echo 'Error: npm is not installed.' >&2
  echo 'Installing npm'
  sudo apt install npm -y
fi

cd ./web
npm install
sudo npm run build
cd ../

#---------------------------- STARTING TELEGRAM-BOT SERVICE ----------------------------


if ! [ -x "$(command - v python3 /telegramBots/initBot/main.py)"]; then
  echo 'Error: python is not found '
  apt update
  apt install python3.7
fi
pip install --upgrade pip
pip install -r requirements.txt

python3 /telegramBots/initBot/main.py
