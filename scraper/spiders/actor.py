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
        yield scrapy.Request(
            url='https://sacramento.craigslist.org/search/cto?postedToday=1&bundleDuplicates=1&searchNearby=2&nearbyArea=63&nearbyArea=187&nearbyArea=43&nearbyArea=373&nearbyArea=709&nearbyArea=189&nearbyArea=675&nearbyArea=216&nearbyArea=454&nearbyArea=285&nearbyArea=96&nearbyArea=102&nearbyArea=188&nearbyArea=92&nearbyArea=191&nearbyArea=62&nearbyArea=710&nearbyArea=1&nearbyArea=708&nearbyArea=97&nearbyArea=707&nearbyArea=346&nearbyArea=456&min_price=2000&min_auto_year=1980',
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
                nextpage = response.xpath(next_page.get('xpath')[0]).get()
                if nextpage:
                    yield response.follow(nextpage, callback=self.parse, headers=self.headers)

    def parse_detail_page(self, response):
        data = {'url': response.url}
        fields = self.config.get('detail_page').get('fields')

        for field in fields:
            key = field.get('name')
            if field.get('selectors').get('regex'):
                value = re.findall(field.get('selectors').get('regex')[0], response.text)
            else:
                xpath = field.get('selectors').get('xpath')[0] + '/' + field.get('selectors').get('extract')
                value = response.xpath(xpath).get()
            data.update({key: value})

        yield data
