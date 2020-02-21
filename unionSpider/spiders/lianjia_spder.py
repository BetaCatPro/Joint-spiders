# -*- coding: utf-8 -*-
import scrapy
from scrapy import Request
from unionSpider.items import UnionItem

from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule


class HomeSpider(CrawlSpider):
    name = 'lianjia'
    allowed_domains = ['lianjia.com']
    start_urls = ['https://cd.lianjia.com/ershoufang/']

    rules = {
        # 房产详情链接
        Rule(LinkExtractor(
            restrict_xpaths="//ul[@class='sellListContent']/li/div[@class='info clear']/div[@class='title']/a"),
            follow=True, callback="process_item"),
        # 翻页链接
        Rule(LinkExtractor(
            restrict_xpaths="//div[@class='pagination_group_a']/a"), follow=True),
    }

    def process_item(self, response):
        item = UnionItem()
        # 提取关键字段信息
        item['title'] = response.css('title::text').extract_first()
        item['price'] = response.css(
            'div.overview div.content > div.price > span.total::text').extract_first()
        item['unit_price'] = response.css(
            'div.overview div.content > div.price span.unitPriceValue::text').extract_first()
        item['community_name'] = response.css(
            'div.overview div.content > div.aroundInfo > div.communityName > a::text').extract_first()
        item['region'] = response.css(
            'div.areaName span.info a::text').extract()
        item['type'] = response.css(
            '#introduction div.base ul > li:first-child::text').extract_first()
        item['construction_area'] = response.css(
            '#introduction div.base ul > li:nth-child(3)::text').extract_first()
        item['orientation'] = response.css(
            '#introduction div.base ul > li:nth-child(7)::text').extract_first()
        item['decoration'] = response.css(
            '#introduction div.base ul > li:nth-child(9)::text').extract_first()
        item['floor'] = response.css(
            '#introduction div.base ul > li:nth-child(2)::text').extract_first()
        item['elevator'] = response.css(
            '#introduction div.base ul > li:nth-child(11)::text').extract_first()
        item['purposes'] = response.css(
            '#introduction div.transaction ul > li:nth-child(4) span:nth-child(2)::text').extract_first()
        item['release_date'] = response.css(
            '#introduction div.transaction ul > li:first-child span:nth-child(2)::text').extract_first()
        item['image_urls'] = response.css(
            'div.content-wrapper img::attr(src)').extract()
        item['from_url'] = response.url
        item['house_structure'] = response.css(
            '#introduction div.base ul > li:nth-child(8)::text'
            ).extract_first()
        yield item