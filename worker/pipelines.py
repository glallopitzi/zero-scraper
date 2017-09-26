# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import json
import time
import re
import locale

import datetime

import sys
from scrapy import signals
from scrapy.exporters import JsonItemExporter

import config_loader

ES_DATE_FORMAT = "%Y%m%dT%H%M%SZ"
CONFIG_FOLDER = "config/"

pipeline_settings = config_loader.load_json_from_file('pipeline')


def date_parse(raw_date):
    try:
        for tr in pipeline_settings['date']['to_remove']:
            raw_date = raw_date.replace(tr, "")

        for p in pipeline_settings['date']['pattern']:
            res = datetime.datetime.strptime(raw_date, p)
            if res:
                print "Date found! %s" % res
                return res
    except:
        print sys.exc_info()


class JsonExporterPipeline(object):
    def __init__(self):
        self.files = {}

    @classmethod
    def from_crawler(cls, crawler):
        pipeline = cls()
        crawler.signals.connect(pipeline.spider_opened, signals.spider_opened)
        crawler.signals.connect(pipeline.spider_closed, signals.spider_closed)
        return pipeline

    def spider_opened(self, spider):
        timestr = time.strftime("%Y%m%d-%H%M%S")
        export_filename = 'exports/%s_items.%s.json' % (spider.name, timestr)
        spider.logger.info("export to: %s" % export_filename)
        file = open(export_filename, 'w+b')
        self.files[spider] = file
        self.exporter = JsonItemExporter(file)
        self.exporter.start_exporting()

    def spider_closed(self, spider):
        self.exporter.finish_exporting()
        file = self.files.pop(spider)
        file.close()

    def process_item(self, item, spider):
        self.exporter.export_item(item)
        return item


class DataCleanerPipeline(object):
    CHAR_RE = re.compile('\W+')
    TAG_RE = re.compile(r'<[^>]+>')

    def process_item(self, item, spider):
        for field in item:
            if field != 'location':
                # remove $nbsp; char
                res = item[field].replace(u'\xa0', u' ')

                if field in ['description', 'title', 'date', 'price', 'dimension', 'author', 'city', 'address', 'zone']:
                    res = self.TAG_RE.sub(" ", res).strip()

                if field in ['description', 'title', 'author', 'dimension', 'zone']:
                    res = self.CHAR_RE.sub(" ", res).strip()

                try:
                    item[field] = res.encode('UTF8')
                except:
                    print sys.exc_info()
                    item[field] = 'ENCODING_ERROR'

        return item


class DateCleanerPipeline(object):
    def process_item(self, item, spider):
        raw_date = item['date']
        raw_datetime = datetime.datetime.now()

        if raw_date != "":
            aux_date = date_parse(raw_date)
            if aux_date:
                raw_datetime = aux_date

        item['date'] = raw_datetime.strftime(ES_DATE_FORMAT)
        return item


class PriceCleanerPipeline(object):
    rx = re.compile('\W+')

    def process_item(self, item, spider):
        raw_price = item['price']
        if raw_price != "":
            try:
                clean = re.sub(r'[^0-9' + r']+', '', str(raw_price))
                value = float(clean)
                item['price'] = value
            except:
                item['price'] = 0
        return item


class CityCleanerPipeline(object):
    def process_item(self, item, spider):
        raw_city = item['city']
        raw_address = item['address']
        if raw_city != "":
            try:
                for tr in pipeline_settings['city']['to_remove']:
                    raw_city = raw_city.replace(tr, "")
                item['city'] = raw_city
            except:
                item['city'] = 'STRIP_ERROR'

        # TODO try to get city from address
        if raw_address != "":
            pass

        return item


class DimensionCleanerPipeline(object):
    rx = re.compile('\W+')

    def process_item(self, item, spider):
        raw_dimension = item['dimension']
        if raw_dimension != "":

            for tr in pipeline_settings['dimension']['to_remove']:
                raw_dimension = raw_dimension.replace(tr, "")

            try:
                item['dimension'] = float(raw_dimension)
            except:
                item['dimension'] = 0

        return item


class ZoneCleanerPipeline(object):
    CHAR_RE = re.compile('\W+')

    def process_item(self, item, spider):
        raw_zone = item['zone']
        raw_address = item['address']
        if raw_zone != "":
            try:
                for tr in pipeline_settings['zone']['to_remove']:
                    raw_zone = raw_zone.replace(tr, "")
                item['zone'] = raw_zone
            except:
                item['zone'] = 'STRIP_ERROR'

        # TODO try to get zone from address
        elif raw_address != "" and "\n" in raw_address:
            try:
                raw_address_splitted = raw_address.split("\n")
                item['address'] = raw_address_splitted[0]
                # item['zone'] = raw_address_splitted[1].replace('-', '').strip()
                item['zone'] = self.CHAR_RE.sub(" ", raw_address_splitted[1]).strip()
            except:
                print sys.exc_info()

        return item


class TagsPipeline(object):

    def process_item(self, item, spider):
        try:
            for field in item:
                if field in ['description', 'title', 'city', 'zone']:
                    value = item[field]
                    # TODO use ntlk or es to tokenize etc..?
        except:
            print sys.exc_info()

        return item


class VisitedURLStorePipeline(object):
    files = None

    def __init__(self):
        self.files = {}

    @classmethod
    def from_crawler(cls, crawler):
        pipeline = cls()
        crawler.signals.connect(pipeline.spider_opened, signals.spider_opened)
        crawler.signals.connect(pipeline.spider_closed, signals.spider_closed)
        return pipeline

    def spider_opened(self, spider):
        export_filename = 'exports/%s_crawled_urls' % spider.name
        spider.logger.info("store crawled urls to: %s" % export_filename)
        file = open(export_filename, 'a')
        self.files[spider.name] = file

    def spider_closed(self, spider):
        file = self.files.pop(spider.name)
        file.close()

    def process_item(self, item, spider):
        self.files[spider.name].write(item["url"] + "\n")
        return item
