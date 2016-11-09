from scrapy.crawler import CrawlerRunner, CrawlerProcess
from scrapy.utils.log import configure_logging
from twisted.internet import reactor

from worker.spiders.home_spider import HomeSpider

CRAWLER_TYPE = "process"  # or runner


def launch_crawlers_as_using_runner():
    configure_logging()
    runner = CrawlerProcess({
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
        'ELASTICSEARCH_TYPE': 'items',
    })

    search_obj = {
        'name': 'immobiliare',
        'category': 'appartamenti',
        'region': 'lombardia',
        'ads_type': 'affitti',
        'city': 'Milano'
    }
    runner.crawl(HomeSpider, search_obj=search_obj)

    search_obj = {
        'name': 'trovocasa',
        'category': 'Appartamento',
        'region': 'lombardia',
        'ads_type': 'Affitto',
        'city': 'Milano'
    }
    runner.crawl(HomeSpider, search_obj=search_obj)

    search_obj = {
        'name': 'idealista',
        'category': 'case',
        'region': 'lombardia',
        'ads_type': 'affitto',
        'city': 'milano'
    }
    runner.crawl(HomeSpider, search_obj=search_obj)

    search_obj = {
        'name': 'wikicasa',
        'category': 'appartamento',
        'region': 'lombardia',
        'ads_type': 'affitto',
        'city': 'milano'
    }
    runner.crawl(HomeSpider, search_obj=search_obj)

    search_obj = {
        'name': 'bakeca',
        'category': 'casa',
        'region': 'lombardia',
        'ads_type': 'offro',
        'city': 'milano'
    }
    runner.crawl(HomeSpider, search_obj=search_obj)

    search_obj = {
        'name': 'subito',
        'category': 'appartamenti',
        'region': 'lombardia',
        'ads_type': 'affitto',
        'city': 'milano'
    }
    # yield runner.crawl(HomeSpider, search_obj=search_obj)

    d = runner.join()
    d.addBoth(lambda _: reactor.stop())
    reactor.run()


def launch_crawlers_as_using_process():
    process = CrawlerProcess({
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
        'ELASTICSEARCH_TYPE': 'items',
    })

    search_obj = {
        'name': 'immobiliare',
        'category': 'appartamenti',
        'region': 'lombardia',
        'ads_type': 'affitti',
        'city': 'Milano'
    }
    process.crawl(HomeSpider, search_obj=search_obj)

    search_obj = {
        'name': 'trovocasa',
        'category': 'Appartamento',
        'region': 'lombardia',
        'ads_type': 'Affitto',
        'city': 'Milano'
    }
    process.crawl(HomeSpider, search_obj=search_obj)

    search_obj = {
        'name': 'idealista',
        'category': 'case',
        'region': 'lombardia',
        'ads_type': 'affitto',
        'city': 'milano'
    }
    process.crawl(HomeSpider, search_obj=search_obj)

    search_obj = {
        'name': 'wikicasa',
        'category': 'appartamento',
        'region': 'lombardia',
        'ads_type': 'affitto',
        'city': 'milano'
    }
    process.crawl(HomeSpider, search_obj=search_obj)

    search_obj = {
        'name': 'bakeca',
        'category': 'casa',
        'region': 'lombardia',
        'ads_type': 'offro',
        'city': 'milano'
    }
    process.crawl(HomeSpider, search_obj=search_obj)

    search_obj = {
        'name': 'subito',
        'category': 'appartamenti',
        'region': 'lombardia',
        'ads_type': 'affitto',
        'city': 'milano'
    }
    process.crawl(HomeSpider, search_obj=search_obj)
    process.start()


def launch_crawlers():
    if CRAWLER_TYPE == "process":
        launch_crawlers_as_using_process()
    else:
        launch_crawlers_as_using_runner()



