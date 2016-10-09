#!/bin/bash


eval $(docker-machine env default)

RUNNING=$(docker inspect --format="{{ .State.Running }}" elk 2> /dev/null)
if [ "$RUNNING" == "false" ]; then
    echo "ELK not running"
    exit 2
fi



curl -X GET -H "Cache-Control: no-cache" "http://192.168.99.100:9200/scrapy/_search?pretty" | jq ".hits.hits[]._source.url"