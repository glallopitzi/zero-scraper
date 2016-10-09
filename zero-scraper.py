import json

import scrapy
from elasticsearch import Elasticsearch
from scrapy.crawler import CrawlerProcess

from worker.spiders.base_spider import BaseSpider





# process = CrawlerProcess({
#     # 'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'
# })

# process.crawl(BaseSpider, name='subito', category='appartamenti', region='lombardia', ads_type='affitto', city='milano')
# process.crawl(BaseSpider, name='wikicasa', category='appartamento', region='lombardia', ads_type='affitto', city='milano')
# process.crawl(BaseSpider, name='casa', category='residenziale', region='lombardia', ads_type='affitti', city='milano')

# process.start() # the script will block here until the crawling is finished


es = Elasticsearch([
    {'host': '192.168.99.100'}
])

print es.info()

# print es.indices.exists(index='scrapy')
# print es.count(index='scrapy')

# print json.dumps(es.search(index='scrapy', q='trilocale'))
print json.dumps(es.indices.analyze(index='scrapy'))