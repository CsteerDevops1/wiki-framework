#! /bin/bash

if [ -d "data/db" ]; then
    :
else 
    echo "Creating ./data/db folder"
    mkdir data
    mkdir data/db
fi
sudo chmod -R a+rwx data/db
# for filename in data/**/
# do 
#     echo $filename
#     if [ $(stat -c "%A" "$filename") != "drwxrwxrwx" -a $(stat -c "%A" "$filename") != "-rwxrwxrwx" ]; then
#         echo "Setting rwx on : $filename"
#         sudo chmod a+rwx $filename
#     fi 
# done 

echo "Launching docker-compose"
docker-compose up --build