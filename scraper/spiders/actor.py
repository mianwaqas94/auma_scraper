import scrapy


class ActorSpider(scrapy.Spider):
    name = 'actor'
    allowed_domains = ['assa.com']
    start_urls = ['http://assa.com/']

    def parse(self, response):
        pass
