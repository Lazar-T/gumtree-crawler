# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class GumtreeItem(scrapy.Item):
    name = scrapy.Field()
    location = scrapy.Field()
    sender = scrapy.Field()
    description = scrapy.Field()
    job_type = scrapy.Field()
