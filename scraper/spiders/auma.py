# -*- coding: utf-8 -*-
import scrapy
from scrapy.spiders import Spider
import re


class AumaSpider(Spider):
    name = 'auma'

    def __init__(self, urls, headers, *args, **kwargs):
        """
        This method initializes spiders with start urls
        """
        self.urls = urls
        self.headers = headers

        super(AumaSpider, self).__init__(*args, **kwargs)

    def start_requests(self):
        """
        This method yields the start url
        """
        for url in self.urls:
            yield scrapy.Request(
                url=url,
                callback=self.parse,
                headers=self.headers)

    def parse(self, response):
        """
        This method gets each exhibitionn url, parse the web page and yield the required data
        """
        record = {
            'url': response.url
        }

        title = response.xpath('//h1[@id="tradeFairTitel"]/text()').get()

        record.update({
            'title': title
        })

        yield record
