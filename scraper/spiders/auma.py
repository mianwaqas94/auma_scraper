# -*- coding: utf-8 -*-
import scrapy
from scrapy.spiders import Spider


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
        long_title = response.xpath('//span[@id="lblTradefairTitleLong"]/text()').get()
        if long_title:
            title = title + " - " + long_title
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

        statistics = response.xpath('//div[contains(@class,"stats-table")]/table/tbody/tr[contains(@class, "level-")]')

        for stat in statistics:
            name = stat.xpath('./td[contains(@data-label,"Kennzah")]/text()').get()
            dates = stat.xpath('./td[contains(@data-label,"/")]')

            if name == 'domestic':
                name = stat.xpath('./preceding-sibling::tr[1]/td[1]/text()').get() + " - " + name

            elif name == 'foreign':
                name = stat.xpath('./preceding-sibling::tr[2]/td[1]/text()').get() + " - " + name

            for d in dates:
                key = name + " " + d.xpath('./@data-label').get()
                value = d.xpath('./text()').get()
                record.update({
                    key: value
                })

        exhibitors_profile = response.xpath('//div[contains(@class,"accordion detail-view")]//h5[contains(text(), "Exhibitors profile")]/parent::div/following-sibling::div//text()').getall()
        if exhibitors_profile:
            exhibitors_profile = ', '.join(exhibitors_profile)
        else:
            exhibitors_profile = None

        proportion_of_trade_visitors = response.xpath('//strong[text()="Proportion of trade visitors"]/following-sibling::span/text()').get()
        distance_to_home = response.xpath('//span[text()="Distance to home (%)"]/following-sibling::ul/li')
        distance_to_home_json = {}

        for dist in distance_to_home:
            distance_to_home_json.update({
                dist.xpath('./text()').get(): dist.xpath('./span/text()').get()
            })
        economic_sector = response.xpath('//span[text()="Economic sector (%)"]/following-sibling::ul/li')
        economic_sector_json = {}

        for eco in economic_sector:
            economic_sector_json.update({
                eco.xpath('./text()').get(): eco.xpath('./span/text()').get()
            })

        professional_position = response.xpath('(//span[text()="Professional position (%)"]/following-sibling::ul/li)')
        professional_position_json = {}

        for pro in professional_position:
            professional_position_json.update({
                pro.xpath('./text()').get(): pro.xpath('./span/text()').get()
            })

        average_length_of_stay = response.xpath('//span[text()="Average length of stay (days)"]/following-sibling::p/text()').get()

        frequency_of_trade = response.xpath('(//span[text()="Frequency of trade fair visits (%)"]/following-sibling::ul/li)')
        frequency_of_trade_json = {}

        for freq in frequency_of_trade:
            frequency_of_trade_json.update({
                freq.xpath('./text()').get(): freq.xpath('./span/text()').get()
            })

        influence_of_purchasing = response.xpath(
            '//span[text()="Influence on purchasing/procurement decisions (%)"]/following-sibling::ul/li')
        influence_of_purchasing_json = {}

        for infl in influence_of_purchasing:
            influence_of_purchasing_json.update({
                infl.xpath('./text()').get(): infl.xpath('./span/text()').get()
            })

        size_of_company_organization = response.xpath('//span[text()="Size of company/organization (%)"]/following-sibling::ul/li')
        size_of_company_organization_json = {}

        for size in size_of_company_organization:
            size_of_company_organization_json.update({
                size.xpath('./text()').get(): size.xpath('./span/text()').get()
            })

        foreign_origin_detail = response.xpath('//span[text()="Foreign origin total (%)"]/following-sibling::ul/li')
        foreign_origin_detail_json = {}

        for f in foreign_origin_detail:
            foreign_origin_detail_json.update({
                f.xpath('./text()').get(): f.xpath('./span/text()').get()
            })

        foreign_origin_total = response.xpath('//span[text()="Foreign origin total (%)"]/span/text()').get()

        record.update({
            'exhibitors_profile': exhibitors_profile,
            'proportion_of_trade_visitors': proportion_of_trade_visitors,
            'distance_to_home': distance_to_home_json,
            'economic_sector': economic_sector_json,
            'professional_position': professional_position_json,
            'average_length_of_stay': average_length_of_stay,
            'frequency_of_trade_fair_visit': frequency_of_trade_json,
            'influence_on_purchasing_procurement_decisions': influence_of_purchasing_json,
            'size_of_company_organization': size_of_company_organization_json,
            'foreign_origin_detail': foreign_origin_detail_json,
            'foreign_origin_total': foreign_origin_total
        })

        yield record
