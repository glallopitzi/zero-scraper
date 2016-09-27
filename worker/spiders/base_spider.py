# -*- coding: utf-8 -*-
from ConfigParser import SafeConfigParser, RawConfigParser

import scrapy

from worker.items import Ad


class BaseSpider(scrapy.Spider):

    parser = None
    name = 'base_spider'

    custom_settings = {
        'USER_AGENT': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:40.0) Gecko/20100101 Firefox/40.1',
    }

    def __init__(self, name=None, region=None, ads_type=None, city=None, *args, **kwargs):
        super(BaseSpider, self).__init__(*args, **kwargs)

        self.load_config(name)

        self.name = name
        self.allowed_domains = [self.parser.get(name, 'allowed_domains')]
        self.start_urls = [self.parser.get(name, 'start_urls') % (region, ads_type, region, city)]

    def parse(self, response):
        self.logger.info('A response from %s just arrived!', response.url)

        # ad_titles = response.xpath(self.parser.get('spider', 'items_list') + '/text()').extract()
        ad_urls = response.xpath(self.parser.get(self.name, 'items_list') + '/@href').extract()

        for url in ad_urls:
            yield scrapy.Request(url, callback=self.parse_ads)

    def parse_ads(self, response):
        title = response.xpath(self.parser.get(self.name, 'title') + '/text()').extract_first().encode('UTF8')
        description = response.xpath(self.parser.get(self.name, 'description') + '/text()').extract_first().encode(
            'UTF8')
        # price = response.xpath(self.parser.get(self.name, 'price') + '/text()').extract_first().encode(
        #     'UTF8')
        date = response.xpath(self.parser.get(self.name, 'date') + '/text()').extract_first().encode('UTF8')
        author = response.xpath(self.parser.get(self.name, 'author') + '/text()').extract_first().encode('UTF8')
        yield Ad(title=title, description=description, date=date, author=author)

    def load_config(self, name):
        self.parser = RawConfigParser()
        self.parser.read('../../config/spiders.cfg')
        self.logger.info('Config for %s loaded, found %s items' % (self.name, len(self.parser.items(name))))