from worker.spiders.base_spider import BaseSpider


class MotorSpider(BaseSpider):
    
    parser = None
    name = 'motor_spider'
    args = None
    max_pages = 0
    already_seen_urls = []

    custom_settings = {
        'USER_AGENT': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:40.0) Gecko/20100101 Firefox/40.1',
    }

    def __init__(self, name=None, category=None, region=None, ads_type=None, city=None, *args, **kwargs):
        super(BaseSpider, self).__init__(*args, **kwargs)

        self.args = dict(name=name, category=category, region=region, ads_type=ads_type, city=city)

        self.name = name
        self.load_config('home', name)
        self.allowed_domains = [self.parser.get('general', 'allowed_domains')]
        self.get_already_seen_urls()
        self.start_urls = [self.get_start_urls_from_template()]
