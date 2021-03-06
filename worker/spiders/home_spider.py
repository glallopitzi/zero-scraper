import logging

from worker.items import HomeAd
from worker.spiders.base_spider import BaseSpider


class HomeSpider(BaseSpider):

    parser = None
    name = 'home_spider'
    args = None
    max_pages = 0
    already_seen_urls = []

    logger = logging.getLogger('zero_logger')

    custom_settings = {
        'USER_AGENT': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:40.0) Gecko/20100101 Firefox/40.1',
    }

    def __init__(self, search_obj=None, *args, **kwargs):
        super(BaseSpider, self).__init__(*args, **kwargs)

        self.args = self.parse_search_obj(search_obj, kwargs)

        self.name = self.args['name']
        self.max_pages = self.args['max_pages']
        self.load_config('home', self.args['name'])
        self.allowed_domains = [self.parser.get('general', 'allowed_domains')]

        ## prevent elk querying
        self.get_already_seen_urls()

        self.start_urls = [self.get_start_urls_from_template()]

    def parse_ads(self, response):
        self.logger.info('Parse function called on %s', response.url)

        self.save_html_page(response)
        to_add = self.extract_all_fields(response)
        yield HomeAd(to_add)
