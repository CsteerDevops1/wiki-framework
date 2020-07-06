if [ "$1" != "" ]; then
    DUMP_DIR="$1"
else
    DUMP_DIR="$(pwd)"
fi

docker-compose -f wiki_project/docker-compose.yml exec -T mongo mongodump --archive --gzip > $DUMP_DIR/mongodb_dump_$(date +"%F-%T").gz
