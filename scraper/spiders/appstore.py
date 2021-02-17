# -*- coding: utf-8 -*-
import scrapy
from scrapy.spiders import Spider
import re


class AppstoreSpider(Spider):
    name = 'appstore'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 11_0_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36',
    }

    def __init__(self, cat_url, *args, **kwargs):
        """
        This method initializes spiders with start url
        """
        characters = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S',
                      'T', 'U', 'V', 'W', 'X', 'Y', 'Z', '*']
        # making urls for each character
        self.a_to_z_urls = [f'{cat_url}?letter={c}' for c in characters]

        super(AppstoreSpider, self).__init__(*args, **kwargs)

    def start_requests(self):
        """
        This method yields the start url
        """
        for url in self.a_to_z_urls:
            yield scrapy.Request(
                url=url,
                callback=self.parse,
                headers=self.headers)

    def parse(self, response):
        """
        This method parse apps pages url and yield the requests
        """
        urls = response.xpath('//div[@id="selectedcontent"]//li/a/@href').extract()

        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse_page, headers=self.headers)

        # pagination
        next_page = response.xpath('//ul[@class="list paginate"][1]//li/a[text()="Next"]/@href').get()
        if next_page:
            yield response.follow(next_page, callback=self.parse, headers=self.headers)

    def parse_page(self, response):

        # List of all names in the app store
        name = response.xpath('//h1[@class="product-header__title app-header__title"]/text()').extract_first().strip()
        seller_link = response.xpath('//h2[@class="product-header__identity app-header__identity"]/a/@href').get()
        rows = response.xpath('//div[@class="information-list__item l-row"]')

        info_dict = {'app_url': response.url, 'title': name}

        for row in rows:
            try:
                key = row.xpath('./dt/text()').extract_first().strip()
                if key == 'In-App Purchases':
                    continue
            except:
                continue

            try:
                value = row.xpath('./dd/text()').extract_first().strip()
            except:
                continue

            info_dict.update({key: value})
            if key == 'Seller':
                info_dict.update({'Seller Link': seller_link})

        info_dict['Category'] = rows[2].xpath('./dd/a/text()').extract_first().strip()
        info_dict['Compatibility'] = rows[3].xpath('./dd//p/text()').extract_first().strip()
        info_dict['Languages'] = rows[4].xpath('./dd//p/text()').extract_first()

        review_count = None
        review_count_raw = re.search('reviewCount":(.*)},', response.text)
        if review_count_raw:
            review_count = review_count_raw.group(1)

        rating_value = None
        rating_value_raw = re.search('ratingValue":(.*),"reviewCount', response.text)
        if rating_value_raw:
            rating_value = rating_value_raw.group(1)

        info_dict.update({'review count': review_count, 'rating value': rating_value})
        yield info_dict
