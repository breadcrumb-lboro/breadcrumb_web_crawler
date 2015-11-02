import urlparse
from scrapy.linkextractors import LinkExtractor
from scrapy.selector import HtmlXPathSelector
from scrapy.spiders import CrawlSpider, Rule
import time
from breadcrumb_web_crawler.items import WebContentItem
from bs4 import BeautifulSoup

BASE_URL = 'http://www.lboro.ac.uk'


class BreadcrumbWebSpider(CrawlSpider):
    name = 'breadcrumbWebSpider'
    allowed_domains = ['lboro.ac.uk']
    start_urls = ['http://www.lboro.ac.uk']
    rules = [Rule(LinkExtractor(), callback='parse_website', follow=True)]

    def parse_website(self, response):
        hxs = HtmlXPathSelector(response)
        item = WebContentItem()
        # Extract title
        item['title'] = hxs.select('//header/h1/text()').extract()

        # Extract the tags
        item['tag'] = hxs.select('//header/div[@class=\'post-data\']/p/a/text()').extract()  # Xpath selector for tag(s)


        # Extract the link
        item['url'] = response.url

        content_list_html = hxs.select('//body').extract()

        content_list_text = []

        for content_html in content_list_html:
            soup = BeautifulSoup(content_html)
            content_list_text.append(soup.get_text().strip())

        time.sleep(2)
        # Extract all plain text
        item['content'] = content_list_text

        return item
