# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class Ad(scrapy.Item):
    url = scrapy.Field()
    website = scrapy.Field()
    title = scrapy.Field()
    description = scrapy.Field()
    address = scrapy.Field()
    lat = scrapy.Field()
    lng = scrapy.Field()
    price = scrapy.Field()
    date = scrapy.Field()
    author = scrapy.Field()
    dimension = scrapy.Field()
    categories = []


class AdCategory(scrapy.Item):
    title = scrapy.Field()
    description = scrapy.Field()