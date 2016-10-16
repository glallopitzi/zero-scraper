import argparse
import json

import scrapy
from elasticsearch import Elasticsearch
from scrapy.crawler import CrawlerProcess

from worker.spiders.base_spider import BaseSpider

parser = argparse.ArgumentParser(description='Zero scraper!')

parser.add_argument('--action', '-a',
                    help='choose your action',
                    choices=['create', 'delete', 'reset', 'crawl', 'health-check'],
                    required=True)

args = parser.parse_args()


# # print es.indices.exists(index='scrapy')
# # print es.count(index='scrapy')
# already_seen_url = []
# res = es.search(index='scrapy', filter_path=['hits.hits._source.url'], q='website:subito.it', size=1000)
# for elem in res['hits']['hits']:
#     already_seen_url.append(elem['_source']['url'])
#
# # res_string = json.dumps(res)
# # res_obj = json.loads(res_string)
# # print res_obj['hits']
# # for url in res_obj['hits']['hits']:
# #     print url
# # print json.dumps(es.indices.analyze(index='scrapy'))

def crawl():
    process = CrawlerProcess({
        'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)',
        'ITEM_PIPELINES': {
            'worker.pipelines.DataCleanerPipeline': 500,
            'worker.pipelines.PriceCleanerPipeline': 501,
            # 'worker.pipelines.VisitedURLStorePipeline': 510,
            # 'worker.pipelines.JsonExporterPipeline': 511,
            'scrapyelasticsearch.scrapyelasticsearch.ElasticSearchPipeline': 700
        },
        'ELASTICSEARCH_SERVERS': ['http://local.docker.dev/'],
        'ELASTICSEARCH_PORT': 9200,
        'ELASTICSEARCH_INDEX': 'scrapy',
        'ELASTICSEARCH_TYPE': 'items',
    })

    # process.crawl(BaseSpider, name='subito', category='appartamenti', region='lombardia', ads_type='affitto',
    #               city='milano')
    # process.crawl(BaseSpider, name='wikicasa', category='appartamento', region='lombardia', ads_type='affitto',
    #               city='milano')
    # process.crawl(BaseSpider, name='casa', category='residenziale', region='lombardia', ads_type='affitti',
    #               city='milano')
    # process.crawl(BaseSpider, name='bakeca', category='casa', region='lombardia', ads_type='offro',
    #               city='milano')
    process.crawl(BaseSpider, name='immobiliare', category='appartamenti', region='lombardia', ads_type='affitti',
                  city='Milano')
    # process.crawl(BaseSpider, name='idealista', category='case', region='lombardia', ads_type='affitto',
    #               city='milano')
    # process.crawl(BaseSpider, name='trovocasa', category='Appartamento', region='lombardia', ads_type='Affitto',
    #               city='Milano')

    process.start()  # the script will block here until the crawling is finished


def health_check():
    es = Elasticsearch([{'host': 'local.docker.dev'}])
    print es.info()


def reset_index():
    es = Elasticsearch([{'host': 'local.docker.dev'}])
    print es.indices.delete("scrapy")
    print es.indices.create(index='scrapy', ignore=400)


def delete_index():
    es = Elasticsearch([{'host': 'local.docker.dev'}])
    print es.indices.delete("scrapy")


def create_index():
    es = Elasticsearch([{'host': 'local.docker.dev'}])
    print es.indices.create(index='scrapy', ignore=400)


actions = {
    "create": create_index,
    "delete": delete_index,
    "reset": reset_index,
    "crawl": crawl,
    "health-check": health_check
}

if args.action:
    actions[args.action]()
