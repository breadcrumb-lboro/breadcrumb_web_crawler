from spiders.web_spider import WeansyWebScraper
from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings
from twisted.internet import reactor
from scrapy import log
from scrapy.utils.project import get_project_settings

process = CrawlerProcess(get_project_settings())

# 'followall' is the name of one of the spiders of the project.

spider1 = WeansyWebScraper()

process.crawl(spider1)

process.start()  # the script will block here until the crawling is finished
