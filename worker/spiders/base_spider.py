# -*- coding: utf-8 -*-
import re
from ConfigParser import SafeConfigParser, RawConfigParser

import scrapy

from worker.items import Ad


class BaseSpider(scrapy.Spider):

    parser = None
    name = 'base_spider'

    custom_settings = {
        'USER_AGENT': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:40.0) Gecko/20100101 Firefox/40.1',
    }

    def __init__(self, name=None, category=None, region=None, ads_type=None, city=None, *args, **kwargs):
        super(BaseSpider, self).__init__(*args, **kwargs)

        self.load_config(name)

        self.name = name
        self.allowed_domains = [self.parser.get(name, 'allowed_domains')]

        # FIXME configurable arguments for url starting points
        self.start_urls = [self.parser.get(name, 'start_urls') % (ads_type, category, city)]

    def parse(self, response):
        self.logger.info('A response from %s just arrived!', response.url)

        # ad_titles = response.xpath(self.parser.get('spider', 'items_list') + '/text()').extract()
        ad_urls = response.xpath(self.parser.get(self.name, 'items_list') + '/@href').extract()

        for url in ad_urls:
            yield scrapy.Request(url, callback=self.parse_ads)

    def parse_ads(self, response):
        url = response.url
        title = self.extract_field_text(response, 'title')
        description = self.extract_field_text(response, 'description')
        price = self.extract_field_text(response, 'price')
        price = re.sub(r'[^\w]', '', price).strip()
        date = self.extract_field_text(response, 'date')
        author = self.extract_field_text(response, 'author')
        yield Ad(url=url, title=title, description=description, price=price, date=date, author=author)

    def load_config(self, name):
        self.parser = RawConfigParser()
        self.parser.read('../../config/spiders.cfg')
        self.logger.info('Config for %s loaded, found %s items' % (self.name, len(self.parser.items(name))))

    def extract_field_text(self, response, name):
        res = ""
        if self.parser.get(self.name, name) != '':
            res = response.xpath(self.parser.get(self.name, name) + '/text()').extract_first().encode('UTF8')
        return res
