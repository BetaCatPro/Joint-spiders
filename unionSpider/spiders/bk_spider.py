# -*- coding: utf-8 -*-
import re
import math

import scrapy
from unionSpider.items import UnionItem
from scrapy_redis.spiders import RedisSpider

class BkSpiderSpider(RedisSpider):
# class BkSpiderSpider(scrapy.Spider):
    name = 'bk'
    allowed_domains = ['ke.com']
    # start_urls = ['https://cd.ke.com/ershoufang/']
    redis_key = 'bk:start_urls'
    # lpush bk:start_urls 'https://cd.ke.com/ershoufang/'
    def parse(self, response):
        # 获取该城市二手房界面的首页链接
        index = response.xpath(
            "//*[@id='beike']/div[1]/div[1]/div/ul/li[2]/a/@href").extract()[0].replace('/ershoufang/', '')
        # 获取该城市各区县二手房界面的首页链接
        # hrefs = response.xpath("//*[@class=' CLICKDATA']/@href").extract()
        # for href in hrefs:
        #     # 构造该城市各区县二手房信息列表的链接
        #     url = '%s%s' % (index, href)
        #     yield scrapy.Request(url, callback=self.parse_url,meta={'url':url}, dont_filter=True)
        # url = 'https://cd.ke.com/ershoufang/jinjiang/' finished
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
        url = 'https://cd.ke.com/ershoufang/jintang/'
        # url = 'https://cd.ke.com/ershoufang/pujiang/' fininshed
        # url = 'https://cd.ke.com/ershoufang/qionglai/' fininshed
        yield scrapy.Request(url, callback=self.parse_url,meta={'url':url})

    def parse_url(self, response):
        # 分页爬取
        num = response.xpath('//*[@id="beike"]/div[1]/div[4]/div[1]/div[2]/div[1]/h2/span/text()').get()
        num = int(num)
        print(num)
        page_num = 100 if math.ceil(num / 30) > 100 else math.ceil(num / 30)
        print('*'*20)
        print(page_num)
        print('*'*20)
        for i in range(page_num):
            url = response.meta.get('url')
            url = url + 'pg' + str(i + 1)
            yield scrapy.Request(url, callback=self.parse_item,dont_filter=False)


    def parse_item(self,response):
        for info in response.xpath("//*[@class='info clear']"):
            item_url = info.xpath("./div[1]/a/@href").extract()[0]
            if item_url:
                yield scrapy.Request(item_url, callback=self.parse_detail, dont_filter=False)


    def parse_detail(self,response):
        item = UnionItem()
        item['title'] = response.css('#beike > div.sellDetailPage > div:nth-child(4) > div.detailHeader.VIEWDATA > div > div > div.title > h1::attr(title)').extract_first()
        item['price'] = response.css(
            '#beike > div.sellDetailPage > div:nth-child(6) > div > div.content > div.price > span.total::text').extract_first()
        item['unit_price'] = response.css(
            '#beike > div.sellDetailPage > div:nth-child(6) > div > div.content > div.price > div.text > div.unitPrice > span::text').extract_first()
        item['community_name'] = response.css(
            '#beike > div.sellDetailPage > div:nth-child(6) > div > div.content > div.aroundInfo > div.communityName > a.info.no_resblock_a::text').extract_first()
        item['region'] = response.css(
            '#beike > div.sellDetailPage > div:nth-child(6) > div > div.content > div.aroundInfo > div.areaName > span.info > a::text').extract()
        item['type'] = response.css(
            '#introduction > div > div > div.base > div.content > ul > li:nth-child(1)::text').extract_first()
        item['construction_area'] = response.css(
            '#introduction > div > div > div.base > div.content > ul > li:nth-child(3)::text').extract_first()
        # error
        if response.css('#introduction > div > div > div.base > div.content > ul > li:nth-child(5) > span::text').extract_first() == '套内面积':
            item['orientation'] = response.css(
                '#introduction > div > div > div.base > div.content > ul > li:nth-child(7)::text').extract_first()
            item['decoration'] = response.css(
                '#introduction > div > div > div.base > div.content > ul > li:nth-child(9)::text').extract_first()
            item['house_structure'] = response.css(
                '#introduction > div > div > div.base > div.content > ul > li:nth-child(8)::text').extract_first()
        else:
            item['orientation'] = response.css(
                '#introduction > div > div > div.base > div.content > ul > li:nth-child(6)::text').extract_first()
            item['decoration'] = response.css(
                '#introduction > div > div > div.base > div.content > ul > li:nth-child(8)::text').extract_first()
            item['house_structure'] = response.css(
                '#introduction > div > div > div.base > div.content > ul > li:nth-child(7)::text').extract_first()
        item['floor'] = response.css(
            '#introduction > div > div > div.base > div.content > ul > li:nth-child(2)::text').extract_first()
        #error
        el1 = response.css('#introduction > div > div > div.base > div.content > ul > li:nth-child(11) > span::text').extract_first()
        el2 = response.css('#introduction > div > div > div.base > div.content > ul > li:nth-child(10) > span::text').extract_first()
        if el1=='配备电梯':
            item['elevator'] = response.css(
            '#introduction > div > div > div.base > div.content > ul > li:nth-child(11)::text').extract_first()
        elif el2=='配备电梯':
            item['elevator'] = response.css(
                '#introduction > div > div > div.base > div.content > ul > li:nth-child(10)::text').extract_first()
        else:
            item['elevator'] = '无'
        purposes = response.css(
            '#introduction > div > div > div.transaction > div.content > ul > li:nth-child(4)::text').extract_first()
        purposes = re.sub(r'\n','',purposes)
        item['purposes'] = purposes.strip()
        release_date = response.css(
            '#introduction > div > div > div.transaction > div.content > ul > li:nth-child(1)::text').extract_first()
        release_date = re.sub(r'\n','',release_date)
        item['release_date'] = release_date.strip()
        item['image_urls'] = response.css(
            '#thumbnail2 > ul > li > img::attr(src)').extract()
        item['from_url'] = response.url
        yield item

