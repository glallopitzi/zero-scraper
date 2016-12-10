# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import time
import re
import locale

import datetime

import sys
from scrapy import signals
from scrapy.exporters import JsonItemExporter


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
            # remove $nbsp; char
            res = item[field].replace(u'\xa0', u' ')
            if field == "description" or field == "title" or field == 'date' or field == 'price' or field == 'dimension':
                res = self.TAG_RE.sub(" ", res).strip()
                if field == "description" or field == "title":
                    res = self.CHAR_RE.sub(" ", res).strip()
            item[field] = res.encode('UTF8')

        return item


class DateCleanerPipeline(object):
    def process_item(self, item, spider):
        raw_date = item['date']
        if raw_date != "":
            try:
                item['date'] = datetime.datetime.strptime(raw_date, "%Y-%m-%d %H:%M:%S")
            except:
                print sys.exc_info()
                item['date'] = int(round(time.time() * 1000))
        else:
            item['date'] = int(round(time.time() * 1000))
        return item


class PriceCleanerPipeline(object):
    rx = re.compile('\W+')

    def process_item(self, item, spider):
        raw_price = item['price']
        if raw_price != "":
            # strip "al mese" related
            clean = re.sub(r'[^0-9' + r']+', '', str(raw_price))
            value = float(clean)
            item['price'] = value
        return item


class DimensionCleanerPipeline(object):
    rx = re.compile('\W+')

    def process_item(self, item, spider):
        raw_dimension = item['dimension']
        if raw_dimension != "":
            clean = raw_dimension.replace("m 2", "")
            value = float(clean)
            item['dimension'] = value
        return item


class GeoDataPipeline(object):
    def process_item(self, item, spider):
        raw_lat = item['lat']
        raw_lon = item['lng']

        if raw_lat != "" and raw_lon != "":
            item['location'] = {
                "lat": float(raw_lat),
                "lon": float(raw_lon)
            }

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
