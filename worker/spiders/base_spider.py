# -*- coding: utf-8 -*-
from ConfigParser import SafeConfigParser

import scrapy


class BaseSpider(scrapy.Spider):
    parser = None

    def load_config(self):
        self.parser = SafeConfigParser()
        self.parser.read('../../config/%s.cfg' % self.name)
        self.logger.info('Config for %s loaded, found %s items' % (self.name,  len(self.parser.items('spider'))))
