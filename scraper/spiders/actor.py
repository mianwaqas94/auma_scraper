import scrapy
import json
import re
import datetime


class ActorSpider(scrapy.Spider):
    name = 'actor'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 11_1_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36',
    }

    def __init__(self, urls_file_path, config_file_path, *args, **kwargs):
        self.urls_file_path = urls_file_path
        self.config_file_path = config_file_path

        with open(self.config_file_path, 'r') as file:
            self.config = json.load(file)

        super(ActorSpider, self).__init__(*args, **kwargs)

    def start_requests(self):
        yield scrapy.Request(url='https://www.pakwheels.com/used-cars/search/-/featured_1/',
                             callback=self.parse,
                             headers=self.headers)

    def parse(self, response):
        if self.config.get('listing_page'):
            selector = self.config.get('listing_page').get('selectors')
            xpath = selector.get('xpath')[0] + '/' + selector.get('extract')
            links = response.xpath(xpath)

            for link in links:
                yield response.follow(link.get(), callback=self.parse_detail_page, headers=self.headers)

            # pagination
            next_page = self.config.get('listing_page').get('pagination').get('next_page')
            if next_page:
                nextpage = response.xpath(next_page.get('xpath')[0] + '/' + next_page.get('extract')).get()
                if next:
                    yield response.follow(nextpage, callback=self.parse, headers=self.headers)

    def parse_detail_page(self, response):
        yield {
            'link': response.url
        }
