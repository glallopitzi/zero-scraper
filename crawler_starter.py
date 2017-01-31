import config_loader

from scrapy.crawler import CrawlerRunner, CrawlerProcess
from scrapy.utils.log import configure_logging
from twisted.internet import reactor
from worker.spiders.generic_spider import GenericSpider
from worker.spiders.home_spider import HomeSpider
from worker.spiders.motor_spider import MotorSpider

CRAWLER_TYPE = "process"  # process or runner

items_lookup_table = {
    "home": HomeSpider,
    "motor": MotorSpider,
    "generic": GenericSpider
}


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
                process.crawl(items_lookup_table[config_loader.get_items_type()], search_obj=crawler)
        else:
            process.crawl(items_lookup_table[config_loader.get_items_type()], search_obj=crawler)
    process.start()


def launch_crawlers(target):
    crawlers_data = config_loader.load_json_from_file('crawlers')
    settings_data = config_loader.load_json_from_file('settings')

    if CRAWLER_TYPE == "process":
        launch_crawlers_as_using_process(target, crawlers_data, settings_data)
    else:
        launch_crawlers_as_using_runner(target, crawlers_data, settings_data)
