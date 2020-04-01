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
git pull origin develop
cd ../

#---------------------------- STARTING CORE SERVICE ----------------------------
if [ -d "~/.volumes/mongo/data/db" ]; then
    :
else
    echo "Creating ~/.volumes/mongo/data/db folder"
    mkdir -p ~/.volumes/mongo/data/db
fi

echo "Launching docker-compose"

touch ./telegramBots/userBot/.env
touch ./telegramBots/initBot/.env
touch ./telegramBots/editBot/.env

# used to config user for mongodb
export UID=${UID}
export GID=${GID}

./docker-compose -f $PROJECT_DIR/docker-compose.yml up --build -d
# # don't use sudo if it's unnecessary
# if ! groups | grep docker &> /dev/null; then
#  sudo ./docker-compose -f ./docker-compose.yml up --build -d
# else
#  docker-compose -f ./docker-compose.yml up --build -d
# fi
