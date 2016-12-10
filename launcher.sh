#!/bin/bash


eval $(docker-machine env default)

RUNNING=$(docker inspect --format="{{ .State.Running }}" elk 2> /dev/null)
if [ "$RUNNING" == "false" ]; then
    echo "ELK not running, try typing: docker start elk"
    exit 2
fi

python zero-scraper.py --a reset

python zero-scraper.py --a crawl subito
python zero-scraper.py --a crawl idealista
python zero-scraper.py --a crawl immobiliare
python zero-scraper.py --a crawl trovocasa
python zero-scraper.py --a crawl wikicasa
python zero-scraper.py --a crawl bakeca
python zero-scraper.py --a crawl astegiudiziarie
python zero-scraper.py --a crawl attico
python zero-scraper.py --a crawl toscano
python zero-scraper.py --a crawl tecnocasa
python zero-scraper.py --a crawl casa
python zero-scraper.py --a crawl professionecasa
python zero-scraper.py --a crawl tecnocasa
python zero-scraper.py --a crawl toscano