if [ "$1" != "" ]; then
    RESTORE_FILE="$1"
else
    echo "Restore file is not specified"
    exit -1
fi

docker-compose -f wiki_project/docker-compose.yml exec -T mongo mongorestore --archive --gzip < $RESTORE_FILE

