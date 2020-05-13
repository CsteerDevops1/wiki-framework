#!/bin/bash

#-------------------- VARIABLES --------------------

GIT_REPOSITORY="https://github.com/CsteerDevops1/wiki-framework"
GIT_BRANCH="develop"

#-------------------- CHECKING DEPENDENCIES --------------------

git --version &> /dev/null && TEST_G=1 || TEST_G=0
docker ps &> /dev/null && TEST_D=1 || TEST_D=0
docker-compose --version &> /dev/null && TEST_DC=1 || TEST_DC=0

#-------------------- UPDATING APT --------------------

if [ $TEST_G -eq 0 -o $TEST_D -eq 0 -o $TEST_DC -eq 0 ]; then
	echo -n "Updating apt - "
	sudo apt update &> /dev/null \
		&& echo "OK" || echo "Failed"
fi

#-------------------- INSTALLING GIT --------------------

if [ $TEST_G -eq 0 ]; then
	echo -n "Installing git - "
	sudo apt install git -y &> /dev/null \
		&& echo "OK" || echo "Failed"
fi

#-------------------- INSTALLING DOCKER --------------------

if [ $TEST_D -eq 0 ]; then
	echo -n "Installing docker - "
	sudo apt install docker.io -y &> /dev/null && \
		sudo usermod -aG docker $USER \
			&& echo "OK" || echo "Failed"
	echo "Please relogin to add current user in docker group"
fi

#-------------------- INSTALLING DOCKER-COMPOSE --------------------

if [ $TEST_DC -eq 0 ]; then
	echo -n "Installing docker-compose - "
	sudo apt install docker-compose -y &> /dev/null \
		&& echo "OK" || echo "Failed"
fi

#-------------------- CLONNING GIT --------------------

if [ "$1" = "" ]; then 
	PROJECT_DIR="wiki-framework"
else
	PROJECT_DIR=$1
fi

if ! [ `ls -A $PROJECT_DIR 2> /dev/null | wc -l` -eq 0 ]; then 
	cd $PROJECT_DIR
	if ! [ "$(git remote get-url origin 2> /dev/null)" = "$GIT_REPOSITORY" ]; then
		echo "Directory $PROJECT_DIR already exists and not empty"
		echo "Please choose another project directory"
		exit
	fi
	cd ../
else
	echo -n "Clonning git into $PROJECT_DIR - "
	git clone -b $GIT_BRANCH $GIT_REPOSITORY $PROJECT_DIR &> /dev/null \
		&& echo "OK" || echo "Failed"
fi

#-------------------- CHECKING ENVIRONMENT --------------------

for env_var in \
	BASIC_AUTH_USERNAME \
	BASIC_AUTH_PASSWORD \
	SECRET_KEY \
	REACT_APP_HOSTNAME \
	TRANSLATOR_API_KEY \
	TG_USERBOT_TOKEN \
	TG_EDITORBOT_TOKEN \
	PROXY_URL \
	PROXY_LOGIN \
	PROXY_PASSWORD
do
	if [ "${!env_var}" = "" ]; then 
		ENV_VARS="$ENV_VARS\n$env_var"
	fi
done

if ! [ "$ENV_VARS" = "" ]; then
	echo -n "Please add environment variables before start project:"
	echo -e "$ENV_VARS"
else
	echo "You are ready to start project!"
fi
