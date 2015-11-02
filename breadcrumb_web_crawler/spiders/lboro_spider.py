__author__ = 'Rawand'

import scrapy


class LboroSpider(scrapy.Spider):
    name = "lboro"
    allowed_domains = ["lboro.ac.uk"]
    start_urls = ["http://www.lboro.ac.uk/services/campus-living/accommodation/",
                  "http://www.lboro.ac.uk/services/campus-living/accommodation/aboutus/"]

    def parse(self, response):
        for sel in response.xpath('//ul/li'):
            title = sel.xpath('a/text()').extract()
            link = sel.xpath('a/@href').extract()
            desc = sel.xpath('text()').extract()
            print title, link, desc
