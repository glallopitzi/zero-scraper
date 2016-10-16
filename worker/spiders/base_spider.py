# -*- coding: utf-8 -*-
import sys
from ConfigParser import RawConfigParser
from string import Template

import scrapy
from elasticsearch import Elasticsearch

from worker.items import Ad


class BaseSpider(scrapy.Spider):
    parser = None
    name = 'base_spider'
    args = None
    max_pages = 0
    already_seen_urls = []

    custom_settings = {
        'USER_AGENT': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:40.0) Gecko/20100101 Firefox/40.1',
    }

    def __init__(self, name=None, category=None, region=None, ads_type=None, city=None, *args, **kwargs):
        super(BaseSpider, self).__init__(*args, **kwargs)

        self.args = dict(name=name, category=category, region=region, ads_type=ads_type, city=city)

        self.name = name
        self.load_config(name)
        self.allowed_domains = [self.parser.get('general', 'allowed_domains')]
        self.get_already_seen_urls()
        self.start_urls = [Template(self.parser.get('general', 'start_urls')).substitute(self.args)]

    def parse(self, response, next_flag=True):
        self.logger.info('A response from %s just arrived!', response.url)
        ad_urls = response.xpath(self.parser.get('general', 'items_list')).extract()
        if self.max_pages > 0:
            self.max_pages -= 1
            next_page_url = response.xpath(self.parser.get('general', 'next_urls')).extract_first()
            next_page_url_string = self.get_absolute_url_string(next_page_url, response)
            yield scrapy.Request(next_page_url_string, callback=self.parse)

        for url in ad_urls:
            url_string = self.get_absolute_url_string(url, response)
            if url_string not in self.already_seen_urls:
                yield scrapy.Request(url_string, callback=self.parse_ads)
            else:
                self.logger.debug("URL %s already crawled" % url_string)

    def parse_ads(self, response):

        to_add = {
            'url': response.url,
            'website': self.parser.get('general', 'allowed_domains'),
        }

        for field_name in self.parser.options('item-selectors'):
            to_add[field_name] = self.extract_field(response, field_name)

        yield Ad(to_add)

    def load_config(self, name):
        self.parser = RawConfigParser()
        config_filename = "config/%s.cfg" % name
        self.parser.read(config_filename)
        self.logger.info('Config for %s loaded from %s, found %s sections' % (config_filename, self.name, len(self.parser.sections())))

    def extract_field(self, response, name):
        res = ""
        try:
            if self.parser.get('item-selectors', name) != '':
                elem = response.xpath(self.parser.get('item-selectors', name))
                if elem is not None:
                    res = elem.extract_first().encode('UTF8')
            return res
        except:
            print sys.exc_info()
            return ""

    def get_absolute_url_string(self, url, response):
        url_string = response.urljoin(url)
        return url_string

    def get_already_seen_urls(self):
        es = Elasticsearch([{'host': 'local.docker.dev'}])
        res = es.search(
            index='scrapy',
            filter_path=['hits.hits._source.url'],
            q='website:' + self.parser.get('general', 'allowed_domains'),
            size=1000
        )
        if res:
            for elem in res['hits']['hits']:
                self.already_seen_urls.append(elem['_source']['url'])
