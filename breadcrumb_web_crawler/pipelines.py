# -*- coding: utf-8 -*-

# Define your item pipelines here
# Pipelines.py is the file used to perform some actions on an item after it has been scraped by the spider. - See more at: http://www.devx.com/webdev/build-a-python-web-crawler-with-scrapy.html#sthash.8GvEr6Je.dpuf
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html


class ScrapyCrawlerExamplePipeline(object):
    def process_item(self, item, spider):
        return item
