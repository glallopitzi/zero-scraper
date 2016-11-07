#!/bin/bash


eval $(docker-machine env default)

RUNNING=$(docker inspect --format="{{ .State.Running }}" elk 2> /dev/null)
if [ "$RUNNING" == "false" ]; then
    echo "ELK not running, try typing: docker start elk"
    exit 2
fi



#auto vendita milano
#scooter vendita milano
#playstation vendita milano

#appartamento affitto milano
#appartamento vendita milano


scrapy crawl home_spider -a name=immobiliare -a category=appartamenti -a ads_type=affitti -a region=lombardia -a city=Milano
scrapy crawl home_spider -a name=subito -a category=appartamenti -a ads_type=affitto -a region=lombardia -a city=milano
scrapy crawl home_spider -a name=astegiudiziarie -a category=appartamenti -a ads_type=affitto -a region=lombardia -a city=milano
scrapy crawl home_spider -a name=bakeca -a category=casa -a ads_type=offro -a region=lombardia -a city=milano
scrapy crawl home_spider -a name=wikicasa -a category=appartamento -a ads_type=affitto -a region=lombardia -a city=milano
scrapy crawl home_spider -a name=idealista -a category=case -a ads_type=affitto -a region=lombardia -a city=milano
scrapy crawl home_spider -a name=attico -a category=appartamenti -a ads_type=vendita -a region=lombardia -a city=milano

#curl -X GET -H "Cache-Control: no-cache" "http://192.168.99.100:9200/scrapy/_search?pretty" | jq ".hits.hits[]._source.url"