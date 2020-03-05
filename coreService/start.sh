#! /bin/bash

if [ -d "data/db" ]; then
    :
else 
    echo "Creating ./data/db folder"
    mkdir data
    mkdir data/db
fi

echo "Launching docker-compose"
export UID=${UID}
export GID=${GID}
docker-compose up --build