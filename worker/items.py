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
    price = scrapy.Field()
    date = scrapy.Field()
    author = scrapy.Field()


class HomeAd(Ad):
    dimension = scrapy.Field()
    address = scrapy.Field()
    lat = scrapy.Field()
    lng = scrapy.Field()


class MotorAd(Ad):
    displacement = scrapy.Field()
    plate = scrapy.Field()
    year = scrapy.Field()

