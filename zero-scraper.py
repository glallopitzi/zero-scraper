import argparse
import json

import scrapy
from elasticsearch import Elasticsearch
from scrapy.crawler import CrawlerProcess

from worker.spiders.base_spider import BaseSpider


parser = argparse.ArgumentParser(description='Zero scraper!')
parser.add_argument("--a")
args = parser.parse_args()

if args.a == 'create':
    es = Elasticsearch([{'host': 'local.docker.dev'}])
    print es.indices.create(index='scrapy', ignore=400)

if args.a == 'delete':
    es = Elasticsearch([{'host': 'local.docker.dev'}])
    print es.indices.delete("scrapy")



# process = CrawlerProcess({
#     # 'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'
# })

# process.crawl(BaseSpider, name='subito', category='appartamenti', region='lombardia', ads_type='affitto', city='milano')
# process.crawl(BaseSpider, name='wikicasa', category='appartamento', region='lombardia', ads_type='affitto', city='milano')
# process.crawl(BaseSpider, name='casa', category='residenziale', region='lombardia', ads_type='affitti', city='milano')

# process.start() # the script will block here until the crawling is finished




# print es.info()


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
