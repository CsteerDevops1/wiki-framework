#!/bin/bash

#-------------------- UPDATING REPOSITORY --------------------

GIT_REPOSITORY="https://github.com/CsteerDevops1/wiki-framework"
GIT_BRANCH="develop"
PROJECT_DIR=$1
if [ "$PROJECT_DIR" = "" ]; then PROJECT_DIR="wiki-framework"; fi
if ! [ `ls -A $PROJECT_DIR 2> /dev/null | wc -l` -eq 0 ]; then 
	cd $PROJECT_DIR
	if [ "$(git remote get-url origin 2> /dev/null)" = "$GIT_REPOSITORY" ]; then
		echo -n "Pulling updates into $PROJECT_DIR - "
		git pull origin $GIT_BRANCH &> /dev/null \
			&& echo "OK" || echo "Failed"
	else
		echo "Directory $PROJECT_DIR is not wiki-framework repository"
		exit
	fi
	cd ../
else
	echo "Project directory $PROJECT_DIR is not exists or empty"
	echo -n "Clonning git repository into $PROJECT_DIR - "
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
	exit
else
	echo "Starting project!"
fi

# Setting UID for MongoDB
if [ "$MONGO_UID" = "" ]; then
	export MONGO_UID=$(id -u)
fi

# Setting GID for MongoDB
if [ "$MONGO_GID" = "" ]; then
	export MONGO_GID=$(id -g)
fi

# Setting DB path for MongoDB
if [ "$MONGO_DATA_PATH" = "" ]; then
	export MONGO_DATA_PATH="~/.volumes/mongo/data/db"
fi

# Setting hostname path for React
if ! [ "$REACT_APP_HOSTNAME" = "" ]; then
	cd $PROJECT_DIR
	echo "REACT_APP_HOSTNAME=$REACT_APP_HOSTNAME" \
		> web/.env
	cd ../
fi

#-------------------- STARTING PROJECT --------------------

# Creating DB directory
if ! [ -d "$MONGO_DATA_PATH" ]; then
    echo -n "Creating $MONGO_DATA_PATH directory - "
    mkdir -p ~/.volumes/mongo/data/db && echo "OK" || echo "Failed"
fi

# Starting project
cd $PROJECT_DIR
docker-compose up --build -d

