# -*- coding: utf-8 -*-
import scrapy
import re
from hourse_area.items import AjkItem

from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule


class AjkSpiderSpider(scrapy.Spider):
    name = 'ajk_spider'
    allowed_domains = ['anjuke.com']
    start_urls = ['https://chengdu.anjuke.com/sale/']

    # rules = [
    #     Rule(LinkExtractor(allow=("https://sz\.fang\.anjuke\.com/loupan/all/p\d{1,}"))),
    #     Rule(LinkExtractor(allow=("https://sz\.fang\.anjuke\.com/loupan/\d{1,}")), follow=False, callback='parse_item')
    # ]


def parse(self, response):
        area_lists = response.css(
            'div.div-border.items-list div.items:first-child .elems-l a')

        area_item = HourseAreaItem()
        display_order = 1
        for item in area_lists:
            href = item.css('::attr(href)').extract_first().strip()

            area_item['code'] = href.replace(
                'https://chongqing.anjuke.com/sale/', '').replace('/', '')
            area_item['name'] = item.css('::text').extract_first().strip()
            area_item['parent_code'] = ''
            area_item['display_order'] = display_order

            display_order += 1

            yield area_item

            yield scrapy.Request(href, callback=self.parse_subarea, meta={'parent_code': area_item['code']})

    def parse_subarea(self, response):
        subarea_lists = response.css('div.div-border.items-list div.items:first-child .elems-l .sub-items a')
        area_item = HourseAreaItem()
        display_order = 1
        for item in subarea_lists:
            href = item.css('::attr(href)').extract_first().strip()

            area_item['code'] = href.replace('https://chongqing.anjuke.com/sale/','').replace('/','')
            area_item['name'] = item.css('::text').extract_first().strip()
            area_item['parent_code'] = response.meta['parent_code']
            area_item['display_order'] = display_order

            display_order += 1

            yield area_item
