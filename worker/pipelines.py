# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import time
import re

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
    rx = re.compile('\W+')

    def process_item(self, item, spider):
        for field in item:
            if field != "url" and field != "website" and field != "date":
                res = item[field]
                res = self.rx.sub(" ", res).strip()
                # print field + ":" + res
                item[field] = res
        return item


class VisitedURLStorePipeline(object):

    url_list_file = None

    def __init__(self):
        self.url_list_file = open("crawled_urls", 'a')

    def process_item(self, item, spider):
        self.url_list_file.write(item["url"])
        return item
