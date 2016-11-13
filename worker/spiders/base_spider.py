# -*- coding: utf-8 -*-
import sys
from ConfigParser import RawConfigParser
from string import Template

import scrapy
from elasticsearch import Elasticsearch

from worker.items import Ad


def extract_field_given_selector(response, field_selector):
    elem = response.xpath(field_selector)
    if elem is not None and elem != []:
        try:
            res = elem.extract_first().encode('UTF8')
            return res
        except:
            print sys.exc_info()
            return ""


def extract_field(response, raw_field_selector):
    res = ""
    if raw_field_selector != '':
        for field_selector in raw_field_selector.split('|'):
            elem = extract_field_given_selector(response, field_selector)
            if elem is not None and elem != '':
                break
    return res


class BaseSpider(scrapy.Spider):
    parser = None
    name = 'base_spider'
    args = None
    max_pages = 0
    already_seen_urls = []

    custom_settings = {
        'USER_AGENT': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:40.0) Gecko/20100101 Firefox/40.1',
    }

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
            to_add[field_name] = extract_field(response, field_name)

        yield Ad(to_add)

    def load_config(self, spider_type, name):
        self.parser = RawConfigParser()
        config_filename = "config/%s/%s.cfg" % (spider_type, name)
        self.parser.read(config_filename)
        self.logger.info('Config %s for type %s loaded from %s, found %s sections' % (config_filename, spider_type, self.name, len(self.parser.sections())))

    def extract_all_fields(self, response):

        to_add = {
            'url': response.url,
            'website': self.parser.get('general', 'allowed_domains'),
        }

        for field_name in self.parser.options('item-selectors'):
            raw_field_selector = self.parser.get('item-selectors', field_name)
            to_add[field_name] = extract_field(response, raw_field_selector)

        return to_add

    @staticmethod
    def get_absolute_url_string(url, response):
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

    def get_start_urls_from_template(self):
        return Template(self.parser.get('general', 'start_urls')).substitute(self.args)

    def parse_search_obj(self, search_obj, kwargs):
        if search_obj is None:
            search_obj = {}
            for name, value in kwargs.items():
                search_obj[name] = value
        return search_obj

