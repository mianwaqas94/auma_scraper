from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from scraper.spiders.actor import ActorSpider
from proxy_rotation.proxy_scraper import create_proxy_list

create_proxy_list()
# c = CrawlerProcess(get_project_settings(), {
#     'FEED_FORMAT': 'json',
#     'FEED_URI': 'output.json'
# })
# c = CrawlerProcess(
#     get_project_settings()
# )
c = CrawlerProcess({
    'FEED_FORMAT': 'json',
    'FEED_URI': 'output.json'
})
c.crawl(ActorSpider, "asfdfd", "config/pakwheels/spider_config.json")
c.start()
