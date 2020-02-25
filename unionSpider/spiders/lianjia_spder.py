# -*- coding: utf-8 -*-
import math

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
        # index = response.xpath(
        #     "/html/body/div[1]/div/ul/li[2]/a/@href").extract()[0].replace('/ershoufang/', '')
        # # 获取该城市各区县二手房界面的首页链接
        # hrefs = response.css("body > div:nth-child(12) > div > div.position > dl:nth-child(2) > dd > div:nth-child(1) > div > a::attr(href)").extract()
        # for href in hrefs:
        #     # 构造该城市各区县二手房信息列表的链接
        #     url = '%s%s/' % (index, href)
        #     yield scrapy.Request(url, callback=self.parse_url, meta={'url':url}, dont_filter=True)
        url = 'https://cd.ke.com/ershoufang/jinjiang/'
        # url = 'https://cd.ke.com/ershoufang/qingyang/'
        # url = 'https://cd.ke.com/ershoufang/wuhou/'
        # url = 'https://cd.ke.com/ershoufang/gaoxin7/'
        # url = 'https://cd.ke.com/ershoufang/chenghua/'
        # url = 'https://cd.ke.com/ershoufang/jinniu/'
        # url = 'https://cd.ke.com/ershoufang/tianfuxinqu/'
        # url = 'https://cd.ke.com/ershoufang/gaoxinxi1/'
        # url = 'https://cd.ke.com/ershoufang/shuangliu/'
        # url = 'https://cd.ke.com/ershoufang/wenjiang/'
        # url = 'https://cd.ke.com/ershoufang/pidu/'
        # url = 'https://cd.ke.com/ershoufang/longquanyi/'
        # url = 'https://cd.ke.com/ershoufang/xindu/'
        # url = 'https://cd.ke.com/ershoufang/tianfuxinqunanqu/'
        # url = 'https://cd.ke.com/ershoufang/qingbaijiang/'
        # url = 'https://cd.ke.com/ershoufang/dujiangyan/'
        # url = 'https://cd.ke.com/ershoufang/pengzhou/'
        # url = 'https://cd.ke.com/ershoufang/jianyang/'
        # url = 'https://cd.ke.com/ershoufang/chongzhou1/'
        # url = 'https://cd.ke.com/ershoufang/dayi/'
        # url = 'https://cd.ke.com/ershoufang/jingtang/'
        # url = 'https://cd.ke.com/ershoufang/pujiang/'
        # url = 'https://cd.ke.com/ershoufang/qionglai/'
        yield scrapy.Request(url, callback=self.parse_url, meta={'url': url})

    def parse_url(self, response):
        # 分页爬取
        num = response.xpath('//*[@id="content"]/div[1]/div[2]/h2/span/text()').get()
        num = int(num)
        page_num = 100 if math.ceil(num / 30) > 100 else math.ceil(num / 30)
        for i in range(page_num):
            url = response.meta.get('url')
            url = url + 'pg' + str(i + 1)
            yield scrapy.Request(url, callback=self.parse_item,dont_filter=False)


    def parse_item(self,response):
        for info in response.xpath("//*[@class='info clear']"):
            item_url = info.xpath("./div[1]/a/@href").extract()[0]
            if item_url:
                yield scrapy.Request(item_url, callback=self.parse_detail, dont_filter=False)

    def parse_detail(self, response):
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