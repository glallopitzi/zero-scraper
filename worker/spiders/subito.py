# -*- coding: utf-8 -*-
import scrapy

from worker.spiders.base_spider import BaseSpider


class SubitoSpider(BaseSpider):
    name = "subito"
    allowed_domains = ["subito.it"]
    start_urls = (
        'http://www.subito.it/',
        # 'http://www.subito.it/annunci-lombardia/vendita/moto-e-scooter/milano/milano/?pe=3&ccs=125&cce=125&mt=4'
    )

    # def parse(self, response):
    #     pass


    def start_requests(self):
        return [scrapy.FormRequest("http://www.subito.it/annunci-lombardia/vendita/moto-e-scooter/milano/milano/",
                                   formdata={'user': 'john', 'pass': 'secret'},
                                   callback=self.logged_in)]


    def logged_in(self, response):
        # here you would extract links to follow and return Requests for
        # each of them, with another callback
        pass