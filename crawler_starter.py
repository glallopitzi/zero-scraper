import json
from pprint import pprint

from scrapy.crawler import CrawlerRunner, CrawlerProcess
from scrapy.utils.log import configure_logging
from twisted.internet import reactor

from worker.spiders.home_spider import HomeSpider

CRAWLER_TYPE = "process"  # or runner

DEFAULT_SETTINGS = {
        'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)',
        'ITEM_PIPELINES': {
            'worker.pipelines.DataCleanerPipeline': 500,
            # 'worker.pipelines.PriceCleanerPipeline': 501,
            'worker.pipelines.DateCleanerPipeline': 502,
            # 'worker.pipelines.VisitedURLStorePipeline': 510,
            # 'worker.pipelines.JsonExporterPipeline': 511,
            'scrapyelasticsearch.scrapyelasticsearch.ElasticSearchPipeline': 700
        },
        'ELASTICSEARCH_SERVERS': ['http://local.docker.dev/'],
        'ELASTICSEARCH_PORT': 9200,
        'ELASTICSEARCH_INDEX': 'scrapy',
        'ELASTICSEARCH_TYPE': 'items'
    }


def launch_crawlers_as_using_runner(data):
    configure_logging()
    runner = CrawlerProcess(DEFAULT_SETTINGS)

    for crawler in data['crawlers']:
        pprint(crawler)
        runner.crawl(HomeSpider, search_obj=crawler)

    d = runner.join()
    d.addBoth(lambda _: reactor.stop())
    reactor.run()


def launch_crawlers_as_using_process(data):
    process = CrawlerProcess(DEFAULT_SETTINGS)

    for crawler in data['crawlers']:
        process.crawl(HomeSpider, search_obj=crawler)

    process.start()


def launch_crawlers(target):
    with open('crawlers.json') as data_file:
        data = json.load(data_file)

    if target == 'all':
        if CRAWLER_TYPE == "process":
            launch_crawlers_as_using_process(data)
        else:
            launch_crawlers_as_using_runner(data)
    else:

        process = CrawlerProcess(DEFAULT_SETTINGS)

        for crawler in data['crawlers']:
            if crawler['name'] == target:
                pprint(crawler)
                process.crawl(HomeSpider, search_obj=crawler)
                process.start()


