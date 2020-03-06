# -*- coding: utf-8 -*-
import scrapy
from scrapy_redis.spiders import RedisSpider
from scrapy.http import Request
from ajk.utils.InsertRedis import inserintotc,inserintota
import re


# class TczufangSpider(RedisSpider):
class TczufangSpider(scrapy.Spider):
    name='ajk'
    start_urls=['https://chengdu.anjuke.com/sale/qonglaishi/']
    # redis_key = 'start_urls'

    # the slaves will get url from ajk:requests

    # url:
    #     邛崃
    #     大邑
    #     崇州
    #     天府新区
    def parse(self, response):
        start_urls = [
            'https://chengdu.anjuke.com/sale/qonglaishi/',
            'https://chengdu.anjuke.com/sale/dayixian/',
            'https://chengdu.anjuke.com/sale/chongzhoushi/',
            'https://chengdu.anjuke.com/sale/tianfuxinqu/'
        ]

        for url in start_urls:
            yield scrapy.Request(url, callback=self.parse_url)

    def parse_url(self,response):
        print(response.xpath("//*[@class='house-details']"))
        for info in response.xpath("//*[@class='house-details']"):
            item_url = info.xpath("./div[1]/a/@href").extract()[0]
            if item_url:
                inserintota(item_url, 2)
                print('ok' + item_url)
        next_url = response.xpath("//*[@id='content']/div[@class='sale-left']/div[@class='multi-page']/a[@class='aNxt']/@href").get()
        if next_url:
            yield scrapy.Request(next_url, callback=self.parse_url)
