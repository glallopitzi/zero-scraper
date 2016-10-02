# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import json
import re


class JsonWriterPipeline(object):

    def __init__(self):
        self.file = open('items.jl', 'a')

    def process_item(self, item, spider):
        line = json.dumps(dict(item)) + "\n"
        self.file.write(line)
        return item


class DataCleanerPipeline(object):
    rx = re.compile('\W+')

    def process_item(self, item, spider):
        for field in item:
            res = item[field]
            res = self.rx.sub(" ", res).strip()
            print field + ":" + res
            item[field] = res
        return item
