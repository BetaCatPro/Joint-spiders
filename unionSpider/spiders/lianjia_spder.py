# -*- coding: utf-8 -*-
import scrapy
from scrapy import Request
from unionSpider.items import UnionItem

from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

from scrapy_redis.spiders import RedisSpider


class HomeSpider(scrapy.Spider):
# class HomeSpider(RedisSpider):
    name = 'lianjia'
    allowed_domains = ['cd.lianjia.com']
    start_urls = ['https://cd.lianjia.com/ershoufang/']
    # redis_key = 'lianjia:start_urls'
    # lpush bk:start_urls 'https://cd.lianjia.com/ershoufang/'

    # rules = {
    #     # 各区县
    #     Rule(LinkExtractor(
    #         restrict_xpaths="//div[@class='ershoufang']/div/a"),
    #         follow=True),
    #     # 房产详情链接
    #     Rule(LinkExtractor(
    #         restrict_xpaths="//ul[@class='sellListContent']/li/div[@class='info clear']/div[@class='title']/a"),
    #         follow=True, callback="process_item"),
    #     # 翻页链接
    #     Rule(LinkExtractor(
    #         restrict_xpaths="//div[@class='pagination_group_a']/a"), follow=True),
    # }

    def parse(self, response):
        # 获取该城市二手房界面的首页链接
        index = response.xpath(
            "/html/body/div[1]/div/ul/li[2]/a/@href").extract()[0].replace('/ershoufang/', '')
        # 获取该城市各区县二手房界面的首页链接
        hrefs = response.css("body > div:nth-child(12) > div > div.position > dl:nth-child(2) > dd > div:nth-child(1) > div > a::attr(href)").extract()
        for href in hrefs:
            # 构造该城市各区县二手房信息列表的链接
            url = '%s%s/' % (index, href)
            yield scrapy.Request(url, callback=self.parse_url, dont_filter=True)

    def parse_url(self, response):
        # 分页爬取
        num = response.css('#content > div.leftContent > div.contentBottom.clear > div.page-box.fr > div > a:nth-child(5)::text').get()
        num = int(num)
        for i in range(num + 1):
            for info in response.css("#content > div.leftContent > ul"):
                item_url = info.xpath("./div[1]/div[@class='title']/a/@href").extract()[0]
                yield scrapy.Request(item_url, callback=self.process_item, dont_filter=True)

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