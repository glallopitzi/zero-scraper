# -*- coding: utf-8 -*-
import scrapy

from worker.items import Ad
from worker.spiders.base_spider import BaseSpider


class SubitoSpider(BaseSpider):

    name = "subito"
    allowed_domains = ["subito.it"]
    custom_settings = {
        'USER_AGENT': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:40.0) Gecko/20100101 Firefox/40.1',
    }

    def __init__(self, region=None, ads_type=None, city=None,  *args, **kwargs):
        super(SubitoSpider, self).__init__(*args, **kwargs)
        self.load_config()
        self.start_urls = ['http://www.subito.it/annunci-%s/%s/appartamenti/%s/%s/' % (region, ads_type, region, city)]

    def parse(self, response):
        self.logger.info('A response from %s just arrived!', response.url)

        # ad_titles = response.xpath(self.parser.get('spider', 'items_list') + '/text()').extract()
        ad_urls = response.xpath(self.parser.get('spider', 'items_list') + '/@href').extract()

        for url in ad_urls:
            yield scrapy.Request(url, callback=self.parse_ads)

    def parse_ads(self, response):
        title = response.xpath(self.parser.get('spider', 'title') + '/text()').extract_first().encode('UTF8')
        description = response.xpath(self.parser.get('spider', 'description') + '/text()').extract_first().encode('UTF8')
        price = response.xpath(self.parser.get('spider', 'price') + '/text()').extract_first().encode(
            'UTF8')

        yield Ad(title=title, description=description, price=price)