from worker.items import HomeAd
from worker.spiders.base_spider import BaseSpider


class HomeSpider(BaseSpider):

    parser = None
    name = 'home_spider'
    args = None
    max_pages = 0
    already_seen_urls = []

    custom_settings = {
        'USER_AGENT': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:40.0) Gecko/20100101 Firefox/40.1',
    }

    def __init__(self, search_obj=None, *args, **kwargs):
        super(BaseSpider, self).__init__(*args, **kwargs)

        self.args = search_obj

        self.name = search_obj['name']
        self.load_config('home', search_obj['name'])
        self.allowed_domains = [self.parser.get('general', 'allowed_domains')]
        self.get_already_seen_urls()
        self.start_urls = [self.get_start_urls_from_template()]

    def parse_ads(self, response):
        to_add = {
            'url': response.url,
            'website': self.parser.get('general', 'allowed_domains'),
        }

        for field_name in self.parser.options('item-selectors'):
            to_add[field_name] = self.extract_field(response, field_name)

        yield HomeAd(to_add)