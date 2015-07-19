# -*- coding: utf-8 -*-
import scrapy
from gumtree.items import GumtreeItem
from scrapy.contrib.loader import ItemLoader
from scrapy.contrib.loader.processor import Compose, MapCompose
from w3lib.html import replace_escape_chars, remove_tags
from scrapy.contrib.spiders import CrawlSpider
from scrapy.http import Request
from scrapy.selector import Selector
import urlparse


class GumtreespiderSpider(CrawlSpider):
    name = "gumtreeSpider"
    allowed_domains = ["gumtree.com.au"]
    seed = 'http://www.gumtree.com.au/s-jobs/page-%d/c9302?ad=wanted'
    start_urls = [
         seed % i for i in range(2000)
    ]

    def parse(self, response):
        hxs = Selector(response)
        item_selector = hxs.xpath('//h3/a/@href').extract()
        job_type_selector = hxs.xpath('//*[@class="rs-ad-attributes h-elips"]/text()').extract()
        for url, job_type in zip(item_selector, job_type_selector):
            yield Request(urlparse.urljoin(response.url, url),
                          callback=self.parse_item,
                          meta={'job_type': job_type},

                          )

    def parse_item(self, response):
        l = ItemLoader(item=GumtreeItem(), response=response)
        l.default_output_processor = MapCompose(lambda v: v.strip(), replace_escape_chars)
        l.add_xpath('name', '//h1/text()')
        location_selector = response.xpath(".//*[@id='ad-map']/span[2]/text()").extract()
        l.add_value('location', location_selector[0])
        sender_selector = response.xpath('//*[@class="reply-form-name"]/text()').extract()
        l.add_value('sender', sender_selector[0])
        l.add_xpath('description', '//*[@id="ad-description"]/text()')
        l.add_value('job_type', response.meta['job_type'])
        return l.load_item()
