from scrapy.crawler import CrawlerProcess
from scraper.spiders.actor import ActorSpider
c = CrawlerProcess({
    'FEED_FORMAT': 'json',
    'FEED_URI': 'output.json',
})
c.crawl(ActorSpider)
c.start()
