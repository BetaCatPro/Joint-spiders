# -*- coding: utf-8 -*-
import scrapy
import re
from unionSpider.items import UnionItem

from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from scrapy.loader import ItemLoader


class AjkSpiderSpider(scrapy.Spider):
    name = 'ajk'
    allowed_domains = ['anjuke.com']
    start_urls = ['https://chengdu.anjuke.com/sale/']

    # 第一次页码标记
    first = True

    def parse(self, response):
        # 验证码处理部分
        pass

        # next page link
        if self.first == True:
            next_url = response.xpath(
                '//*[@id="content"]/div[4]/div[7]/a[7]/@href').extract()[0]
            self.first = False
        else:
            next_url = response.xpath(
                '//*[@id="content"]/div[4]/div[7]/a[8]/@href').extract()[0]
        print('*********' + str(next_url) + '**********')
        if next_url:
            yield scrapy.Request(url=next_url,
                                 callback=self.parse)

        num = len(response.xpath(
            '//*[@id="houselist-mod-new"]/li').extract())

        # for i in range(1, num + 1):
        for i in range(1, 2):
            url = response.xpath(
                '//*[@id="houselist-mod-new"]/li[{}]/div[2]/div[1]/a/@href'
                    .format(i)).extract()[0]
            yield scrapy.Request(url, callback=self.parse_detail)

    def parse_detail(self, response):
        item = UnionItem()
        title = response.css('#content > div.clearfix.title-guarantee > h3::text').extract_first()
        item['title'] = re.sub(r'\n','',title).replace(' ','')
        item['price'] = response.css(
            '#content > div.wrapper > div.wrapper-lf > div.clearfix > div.basic-info.clearfix > span.light.info-tag > em::text').extract_first()
        unit_price = response.css(
            '#content > div.wrapper > div.wrapper-lf > div.houseInfoBox > div > div.houseInfo-wrap > ul > li:nth-child(3) > div.houseInfo-content::text').extract_first()
        item['unit_price'] = unit_price.replace(' 元/m²','')
        item['community_name'] = response.css(
            '#content > div.wrapper > div.wrapper-lf > div.houseInfoBox > div > div.houseInfo-wrap > ul > li:nth-child(1) > div.houseInfo-content > a::text').extract_first()
        item['region'] = response.css(
            '#content > div.wrapper > div.wrapper-lf > div.houseInfoBox > div > div.houseInfo-wrap > ul > li:nth-child(4) > div.houseInfo-content > p > a::text').extract()
        type = response.css(
            '#content > div.wrapper > div.wrapper-lf > div.houseInfoBox > div > div.houseInfo-wrap > ul > li:nth-child(2) > div.houseInfo-content::text').extract_first()
        item['type'] = re.sub(r'\n|\t','',type)
        item['construction_area'] = response.css(
            '#content > div.wrapper > div.wrapper-lf > div.houseInfoBox > div > div.houseInfo-wrap > ul > li:nth-child(5) > div.houseInfo-content::text').extract_first()
        item['orientation'] = response.css(
            '#content > div.wrapper > div.wrapper-lf > div.houseInfoBox > div > div.houseInfo-wrap > ul > li:nth-child(8) > div.houseInfo-content::text').extract_first()
        item['decoration'] = response.css(
            '#content > div.wrapper > div.wrapper-lf > div.houseInfoBox > div > div.houseInfo-wrap > ul > li:nth-child(12) > div.houseInfo-content::text').extract_first()
        item['floor'] = response.css(
            '#content > div.wrapper > div.wrapper-lf > div.houseInfoBox > div > div.houseInfo-wrap > ul > li:nth-child(11) > div.houseInfo-content::text').extract_first()
        item['elevator'] = response.css(
            '#content > div.wrapper > div.wrapper-lf > div.houseInfoBox > div > div.houseInfo-wrap > ul > li:nth-child(14) > div.houseInfo-content::text').extract_first()
        item['purposes'] = response.css(
            '#content > div.wrapper > div.wrapper-lf > div.houseInfoBox > div > div.houseInfo-wrap > ul > li:nth-child(10) > div.houseInfo-content::text').extract_first()
        release_date = response.css(
            '#content > div.wrapper > div.wrapper-lf > div.houseInfoBox > div > div.houseInfo-wrap > ul > li:nth-child(7) > div.houseInfo-content::text').extract_first()
        item['release_date'] = re.sub(r'\n|\t','',release_date)
        item['image_urls'] = response.css(
            'div.img_wrap img::attr(src)').extract()
        item['from_url'] = response.url
        item['house_structure'] = response.css(
            '#introduction div.base ul > li:nth-child(8)::text').extract_first()
        yield item

