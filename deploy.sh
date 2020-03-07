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

if ! [ -x "$(command -v docker-compose)" ]; then
  echo 'Error: docker-compose is not installed.' >&2
  sudo curl -L "https://github.com/docker/compose/releases/download/1.25.4/docker-compose-$(uname -s)-$(uname -m)" \
    -o /usr/local/bin/docker-compose
  sudo chmod +x /usr/local/bin/docker-compose
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

#---------------------------- STARTING CORE SERVICE ----------------------------
if [ -d "coreService/data/db" ]; then
    :
else 
    echo "Creating coreService/data/db folder"
    mkdir coreService/data
    mkdir coreService/data/db
fi

echo "Launching docker-compose"

# used to config user for mongodb
export UID=${UID}
export GID=${GID}

# don't use sudo if it's unnecessary
if ! groups | grep docker &> /dev/null; then 
  sudo docker-compose -f coreService/docker-compose.yml up --build -d
else
  docker-compose -f coreService/docker-compose.yml up --build -d
fi 

#---------------------------- STARTING WEB SERVICE ----------------------------

#---------------------------- STARTING TELEGRAM-BOT SERVICE ----------------------------

