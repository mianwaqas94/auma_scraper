from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from scraper.spiders.appstore import AppstoreSpider
import argparse

# Parse command-line arguments.
parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument(
    '-u',
    '--category_url',
    required=True,
    help="path of spider_config.json")

args = parser.parse_args()

url = args.category_url

s = get_project_settings()

proc = CrawlerProcess(s)

proc.crawl(AppstoreSpider, url)
proc.start()
