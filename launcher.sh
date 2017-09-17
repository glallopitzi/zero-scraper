#!/bin/bash


eval $(docker-machine env default)

RUNNING=$(docker inspect --format="{{ .State.Running }}" elk 2> /dev/null)
if [ "$RUNNING" == "false" ]; then
    echo "ELK not running, try typing: docker start elk"
    exit 2
fi

python zero_scraper.py -a reset -c home

python zero_scraper.py -a crawl -c home subito
python zero_scraper.py -a crawl -c home idealista
python zero_scraper.py -a crawl -c home immobiliare
python zero_scraper.py -a crawl -c home homepal

python zero_scraper.py -a crawl -c home trovocasa
python zero_scraper.py -a crawl -c home wikicasa
python zero_scraper.py -a crawl -c home bakeca
python zero_scraper.py -a crawl -c home astegiudiziarie
python zero_scraper.py -a crawl -c home attico
python zero_scraper.py -a crawl -c home toscano
python zero_scraper.py -a crawl -c home tecnocasa
python zero_scraper.py -a crawl -c home casa
python zero_scraper.py -a crawl -c home professionecasa
python zero_scraper.py -a crawl -c home tecnocasa
python zero_scraper.py -a crawl -c home toscano