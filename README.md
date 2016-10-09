## INTRO ##
This is a configurable scraper (based on python Scrapy library) to scrape info from various websites.

## How to run ##
From command line, run the following command:

```bash
scrapy runspider subito.py -a region=lombardia -a ads_type=affitto -a city=milano
```

## Elasticsearch ##
run your docker elk instance and enable the related pipeline.


## TODO ##

* index list of crawled page items (to prevent duplicates)
* better handling for pagination (ex: wikicasa with p parameter instead of links)
* add more info on crawled items
* define ES index