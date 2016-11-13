import json
from pprint import pprint

from scrapy.crawler import CrawlerRunner, CrawlerProcess
from scrapy.utils.log import configure_logging
from twisted.internet import reactor

from worker.spiders.home_spider import HomeSpider

CRAWLER_TYPE = "runner"  # process or runner
CONFIG_FOLDER = "config/"


def launch_crawlers_as_using_runner(target, data, settings):
    configure_logging()

    for crawler in data['crawlers']:
        if target != 'all':
            if target == crawler['name']:
                runner = CrawlerProcess(settings['spider'])
                runner.crawl(HomeSpider, search_obj=crawler)
        else:
            runner = CrawlerProcess(settings['spider'])
            runner.crawl(HomeSpider, search_obj=crawler)

    d = runner.join()
    d.addBoth(lambda _: reactor.stop())
    reactor.run()


def launch_crawlers_as_using_process(target, data, settings):
    process = CrawlerProcess(settings['spider'])

    for crawler in data['crawlers']:
        if target != 'all':
            if target == crawler['name']:
                process.crawl(HomeSpider, search_obj=crawler)
        else:
            process.crawl(HomeSpider, search_obj=crawler)
    process.start()


def launch_crawlers(target):
    with open(CONFIG_FOLDER + 'crawlers/crawlers.json') as data_file:
        data = json.load(data_file)

    with open(CONFIG_FOLDER + 'settings.json') as data_file:
        settings = json.load(data_file)

    if CRAWLER_TYPE == "process":
        launch_crawlers_as_using_process(target, data, settings)
    else:
        launch_crawlers_as_using_runner(target, data, settings)
