# -*- coding: utf-8 -*-
import re
from ConfigParser import RawConfigParser
from string import Template
from urlparse import urlparse

import scrapy

from worker.items import Ad


class BaseSpider(scrapy.Spider):

    parser = None
    name = 'base_spider'
    args = None
    max_pages = 1
    already_crawled_url = ()

    custom_settings = {
        'USER_AGENT': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:40.0) Gecko/20100101 Firefox/40.1',
    }

    p = re.compile('^(https?://[^/]+/)([^?#]*)?')

    def __init__(self, name=None, category=None, region=None, ads_type=None, city=None, *args, **kwargs):
        super(BaseSpider, self).__init__(*args, **kwargs)

        self.args = dict(name=name, category=category, region=region, ads_type=ads_type, city=city)
        self.name = name
        self.load_config(name)
        self.allowed_domains = [self.parser.get(name, 'allowed_domains')]
        self.start_urls = [Template(self.parser.get(name, 'start_urls')).substitute(self.args)]

    def parse(self, response, next_flag=True):
        self.logger.info('A response from %s just arrived!', response.url)
        ad_urls = response.xpath(self.parser.get(self.name, 'items_list')).extract()
        if self.max_pages > 0:
            self.max_pages -= 1
            next_page_url = response.xpath(self.parser.get(self.name, 'next_urls')).extract_first()
            next_page_url_string = self.get_absolute_url_string(next_page_url, response)
            yield scrapy.Request(next_page_url_string, callback=self.parse)

        for url in ad_urls:
            url_string = self.get_absolute_url_string(url, response)
            yield scrapy.Request(url_string, callback=self.parse_ads)

    def parse_ads(self, response):
        url = response.url
        website = self.parser.get(self.name, 'allowed_domains')

        title = self.extract_field(response, 'title')
        description = self.extract_field(response, 'description')
        price = self.extract_field(response, 'price')
        date = self.extract_field(response, 'date')
        author = self.extract_field(response, 'author')

        yield Ad(url=url, website=website, title=title, description=description, price=price, date=date, author=author)

    def load_config(self, name, BASE_CONFIG_PATH='/Users/gianc/Documents/git/zero-scraper'):
        self.parser = RawConfigParser()
        self.parser.read(BASE_CONFIG_PATH + '/config/spiders.cfg')
        self.logger.info('Config for %s loaded, found %s items' % (self.name, len(self.parser.items(name))))

    def extract_field(self, response, name):
        res = ""
        if self.parser.get(self.name, name) != '':
            res = response.xpath(self.parser.get(self.name, name)).extract_first().encode('UTF8')
        return res

    def get_absolute_url_string(self, url, response):
        url_string = response.urljoin(url)
        self.logger.debug("respose.urljoin: %s" % url_string)
        return url_string
