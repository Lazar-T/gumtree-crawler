# -*- coding: utf-8 -*-
import urlparse

from scrapy import Spider
from scrapy.http import Request
from scrapy.loader import ItemLoader
from scrapy.loader.processors import Compose, MapCompose
from w3lib.html import replace_escape_chars, remove_tags

from gumtree.items import GumtreeItem


class GumtreespiderSpider(Spider):
    name = 'gumtree'
    allowed_domains = ['gumtree.com.au']
    start_urls = ['http://www.gumtree.com.au/s-jobs/c9302?ad=wanted']

    def parse(self, response):
        """Yields each job url and iterates over pages of results.

        @url http://www.gumtree.com.au/s-jobs/c9302?ad=wanted
        @scrapes urls job_types

        """
        # process each job link
        urls = response.xpath('//h6/a/@href').extract()
        job_types = response.xpath(
            './/*[@class="rs-ad-attributes-jobtype_s"]/text()').extract()
        for url, job_type in zip(urls, job_types):
            yield Request(urlparse.urljoin(response.url, url),
                          callback=self.parse_item,
                          meta={'job_type': job_type},
                          )

        # process next page
        next_page_url = response.xpath(
            './/*[@class="rs-paginator-btn next"]/@href').extract_first()
        absolute_next_page_url = response.urljoin(next_page_url)
        request = Request(absolute_next_page_url)
        yield request

    def parse_item(self, response):
        """Returns scraped data from each individual job link."""
        l = ItemLoader(item=GumtreeItem(), response=response)
        l.default_output_processor = MapCompose(lambda v: v.strip(), replace_escape_chars)

        l.add_xpath('name', '//h1/text()')
        l.add_xpath('location', './/*[@id="ad-map"]/span[2]/text()')
        l.add_xpath('sender', '//*[@class="name"]/text()')
        l.add_xpath('description', '//*[@id="job-description"]/p/text()')
        l.add_value('job_type', response.meta['job_type'])

        return l.load_item()
