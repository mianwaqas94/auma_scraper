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
        venue = response.xpath('//article//div[@class="item"]/h4//*[contains(text(),"Venue")]/parent::h4/following-sibling::span/text()').getall()
        dates_all = response.xpath('//article//div[@class="item"]/h4//*[contains(text(),"Dates")]/parent::h4/parent::div//span//text()').getall()
        dates = []
        remove_to_be = ['Interval', 'founded', 'digital']
        for date in dates_all:
            if any(r in date for r in remove_to_be):
                pass
            else:
                dates.append(date)

        interval_raw = response.xpath('//article//div[@class="item"]/h4//*[contains(text(),"Dates")]/parent::h4/parent::div//span[contains(text(),"Interval:")]/text()').get()
        if interval_raw:
            interval = interval_raw.replace('Interval: ', '')
        else:
            interval = None
        founded_in_raw = response.xpath('//article//div[@class="item"]/h4//*[contains(text(),"Dates")]/parent::h4/parent::div//span[contains(text(),"founded in:")]/text()').get()
        if founded_in_raw:
            founded_in = founded_in_raw.replace('founded in: ', '')
        else:
            founded_in = None

        organiser = response.xpath('//article//div[@class="item"]/h4[contains(text(),"Organiser")]/following-sibling::div/div[1]//text()').getall()
        project_team = response.xpath('//article//div[@class="item"]/h4[contains(text(),"Organiser")]/following-sibling::div/div[2]//text()').getall()

        record.update({
            'title': title,
            'venue': venue,
            'dates': dates,
            'interval': interval,
            'founded_in': founded_in,
            'organiser': organiser,
            'project_team': project_team
        })

        side_list = response.xpath('//div[contains(@class, "sidelist")]//div[contains(@class, "info-list")]/div')
        for section in side_list:
            key = section.xpath('./strong/text()').get()
            value = ', '.join(section.xpath('./span//text()').getall())

            record.update({
                key: value
            })

        yield record
