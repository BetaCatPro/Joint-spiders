# -*- coding: utf-8 -*-
import re
import math
import time

import scrapy
from unionSpider.items import UnionItem
from scrapy_redis.spiders import RedisSpider

class BkSpiderSpider(RedisSpider):
    name = 'ke'
    allowed_domains = ['ke.com']
    redis_key = 'ke:start_urls'
    def parse(self, response):
        # 这里是单进程默模式
        # 解析各区县url
        # index = response.xpath(
        #     "//*[@id='beike']/div[1]/div[1]/div/ul/li[2]/a/@href").extract()[0].replace('/ershoufang/', '')
        # hrefs = response.xpath("//*[@class=' CLICKDATA']/@href").extract()
        # for href in hrefs:
        #     url = '%s%s' % (index, href)
        #     yield scrapy.Request(url, callback=self.parse_site)


        # 这里通过分布式进行都页面同时爬取
        # server1: lpush ke:start_urls 'https://cd.ke.com/ershoufang/qingyang/' finished
        # server2: lpush ke:start_urls 'https://cd.ke.com/ershoufang/wuhou/'
        # server3: lpush ke:start_urls 'https://cd.ke.com/ershoufang/gaoxin7/'
        # server4: lpush ke:start_urls 'https://cd.ke.com/ershoufang/chenghua/'
        # server5: lpush ke:start_urls 'https://cd.ke.com/ershoufang/jinniu/'
        # server6: lpush ke:start_urls 'https://cd.ke.com/ershoufang/tianfuxinqu/'
        # server7: lpush ke:start_urls 'https://cd.ke.com/ershoufang/shuangliu/'
        # server8: lpush ke:start_urls 'https://cd.ke.com/ershoufang/wenjiang/'
        # server9: lpush ke:start_urls 'https://cd.ke.com/ershoufang/pidu/'
        # server0: lpush ke:start_urls 'https://cd.ke.com/ershoufang/longquanyi/' finished
        # ......
        url = response.url
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
        purposes = response.css(
            '#introduction > div > div > div.transaction > div.content > ul > li:nth-child(4)::text').extract_first()
        purposes = re.sub(r'\n', '', purposes).strip()
        item['purposes'] = purposes.strip()
        is_inline = False
        is_con_type = False
        inline_area = response.css('#introduction > div > div > div.base > div.content > ul > li:nth-child(5) > span::text').extract_first()
        if inline_area == '套内面积':
            is_inline = True
            if response.css('#introduction > div > div > div.base > div.content > ul > li:nth-child(6) > span::text').extract_first() == '建筑类型':
                is_con_type = True
            else:
                is_con_type = False
        elif inline_area == '建筑类型':
            is_con_type = True

        if is_inline==False and is_con_type==False:
            if purposes == '别墅':
                item['orientation'] = response.css(
                    '#introduction > div > div > div.base > div.content > ul > li:nth-child(4)::text').extract_first()
                item['house_structure'] = response.css(
                    '#introduction > div > div > div.base > div.content > ul > li:nth-child(5)::text').extract_first()
                item['decoration'] = response.css(
                    '#introduction > div > div > div.base > div.content > ul > li:nth-child(6)::text').extract_first()
            else:
                item['orientation'] = response.css(
                    '#introduction > div > div > div.base > div.content > ul > li:nth-child(5)::text').extract_first()
                item['house_structure'] = response.css(
                    '#introduction > div > div > div.base > div.content > ul > li:nth-child(6)::text').extract_first()
                item['decoration'] = response.css(
                    '#introduction > div > div > div.base > div.content > ul > li:nth-child(7)::text').extract_first()
        elif is_inline and is_con_type:
            item['orientation'] = response.css(
                '#introduction > div > div > div.base > div.content > ul > li:nth-child(7)::text').extract_first()
            item['house_structure'] = response.css(
                '#introduction > div > div > div.base > div.content > ul > li:nth-child(8)::text').extract_first()
            item['decoration'] = response.css(
                '#introduction > div > div > div.base > div.content > ul > li:nth-child(9)::text').extract_first()
        else:
            if purposes == '别墅':
                item['orientation'] = response.css(
                    '#introduction > div > div > div.base > div.content > ul > li:nth-child(5)::text').extract_first()
                item['house_structure'] = response.css(
                    '#introduction > div > div > div.base > div.content > ul > li:nth-child(6)::text').extract_first()
                item['decoration'] = response.css(
                    '#introduction > div > div > div.base > div.content > ul > li:nth-child(7)::text').extract_first()
            else:
                item['orientation'] = response.css(
                    '#introduction > div > div > div.base > div.content > ul > li:nth-child(6)::text').extract_first()
                item['house_structure'] = response.css(
                    '#introduction > div > div > div.base > div.content > ul > li:nth-child(7)::text').extract_first()
                item['decoration'] = response.css(
                    '#introduction > div > div > div.base > div.content > ul > li:nth-child(8)::text').extract_first()

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
        release_date = response.css(
            '#introduction > div > div > div.transaction > div.content > ul > li:nth-child(1)::text').extract_first()
        release_date = re.sub(r'\n','',release_date).strip()
        final_time = self.parsetime(release_date)
        item['release_date'] = final_time
        item['image_urls'] = response.css(
            '#thumbnail2 > ul > li > img::attr(src)').extract()
        item['from_url'] = response.url
        yield item

    def parsetime(self,rtime):
        """
        parse 2018年1月10日 to 2018-1-10
        """
        tmp_time = time.strptime(rtime, '%Y年%m月%d日')
        year = str(tmp_time.tm_year)
        month = str(tmp_time.tm_mon)
        day = str(tmp_time.tm_mday)
        final_time = year + '-' + month + '-' + day
        return final_time