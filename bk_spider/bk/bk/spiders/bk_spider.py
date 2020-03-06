# -*- coding: utf-8 -*-
import math

import scrapy
from scrapy_redis.spiders import RedisSpider

from bk.utils.InsertRedis import inserintota

class BkSpiderSpider(RedisSpider):
    name = 'ke'
    allowed_domains = ['ke.com']
    redis_key = 'start_urls'
    def parse(self, response):
        # 解析各区县url
        index = response.xpath(
            "//*[@id='beike']/div[1]/div[1]/div/ul/li[2]/a/@href").extract()[0].replace('/ershoufang/', '')
        hrefs = response.xpath("//*[@class=' CLICKDATA']/@href").extract()
        for href in hrefs:
            url = '%s%s' % (index, href)
            yield scrapy.Request(url, callback=self.parse_site)


    def parse_site(self,response):
        # 解析所有街道url
        streets = response.xpath("//*[@class='position']/dl[2]/dd/div[1]/div[2]/a/@href").getall()
        index = response.xpath(
                "//*[@id='beike']/div[1]/div[1]/div/ul/li[2]/a/@href").extract()[0].replace('/ershoufang/', '')
        for url in streets:
            url = '%s%s' % (index, url)
            yield scrapy.Request(url, callback=self.parse_url,meta={'url':url})


    def parse_url(self, response):
        # 分页爬取
        num = response.xpath('//*[@id="beike"]/div[1]/div[4]/div[1]/div[2]/div[1]/h2/span/text()').get()
        num = int(num)
        print('房源数',num)
        page_num = 100 if math.ceil(num / 30) > 100 else math.ceil(num / 30)
        print('*'*20)
        print('总页数',page_num)
        print('*'*20)
        for i in range(page_num):
            url = response.meta.get('url')
            url = url + 'pg' + str(i + 1)
            yield scrapy.Request(url, callback=self.parse_item,dont_filter=False)


    def parse_item(self,response):
        for info in response.xpath("//*[@class='info clear']"):
            item_url = info.xpath("./div[1]/a/@href").extract()[0]
            if item_url:
                inserintota(item_url, 2)
