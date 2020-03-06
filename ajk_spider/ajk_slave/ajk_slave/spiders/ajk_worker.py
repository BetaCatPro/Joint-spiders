# -*- coding: utf-8 -*-
import re
from scrapy_redis.spiders import RedisSpider
from ajk_slave.items import UnionItem


class AjkWorkerSpider(RedisSpider):
    name = 'ajk_worker'
    allowed_domains = ['anjuke.com']
    redis_key = 'ajk:requests'

    def parse(self, response):
        item = UnionItem()
        title = response.css('#content > div.clearfix.title-guarantee > h3::text').extract_first()
        item['title'] = re.sub(r'\n', '', title).replace(' ', '')
        item['price'] = response.css(
            '#content > div.wrapper > div.wrapper-lf > div.clearfix > div.basic-info.clearfix > span.light.info-tag > em::text').extract_first()
        unit_price = response.css(
            '#content > div.wrapper > div.wrapper-lf > div.houseInfoBox > div > div.houseInfo-wrap > ul > li:nth-child(3) > div.houseInfo-content::text').extract_first()
        item['unit_price'] = unit_price.replace(' 元/m²', '')
        item['community_name'] = response.css(
            '#content > div.wrapper > div.wrapper-lf > div.houseInfoBox > div > div.houseInfo-wrap > ul > li:nth-child(1) > div.houseInfo-content > a::text').extract_first()
        item['region'] = response.css(
            '#content > div.wrapper > div.wrapper-lf > div.houseInfoBox > div > div.houseInfo-wrap > ul > li:nth-child(4) > div.houseInfo-content > p > a::text').extract()
        type = response.css(
            '#content > div.wrapper > div.wrapper-lf > div.houseInfoBox > div > div.houseInfo-wrap > ul > li:nth-child(2) > div.houseInfo-content::text').extract_first()
        item['type'] = re.sub(r'\n|\t', '', type)
        construction_area = response.css(
            '#content > div.wrapper > div.wrapper-lf > div.houseInfoBox > div > div.houseInfo-wrap > ul > li:nth-child(5) > div.houseInfo-content::text').extract_first()
        item['construction_area'] = construction_area.replace('平方米', '㎡')
        item['orientation'] = response.css(
            '#content > div.wrapper > div.wrapper-lf > div.houseInfoBox > div > div.houseInfo-wrap > ul > li:nth-child(8) > div.houseInfo-content::text').extract_first()
        decoration = response.css(
            '#content > div.wrapper > div.wrapper-lf > div.houseInfoBox > div > div.houseInfo-wrap > ul > li:nth-child(12) > div.houseInfo-content::text').extract_first()
        item['decoration'] = decoration.replace('修','')
        item['floor'] = response.css(
            '#content > div.wrapper > div.wrapper-lf > div.houseInfoBox > div > div.houseInfo-wrap > ul > li:nth-child(11) > div.houseInfo-content::text').extract_first()
        item['elevator'] = response.css(
            '#content > div.wrapper > div.wrapper-lf > div.houseInfoBox > div > div.houseInfo-wrap > ul > li:nth-child(14) > div.houseInfo-content::text').extract_first()
        item['purposes'] = response.css(
            '#content > div.wrapper > div.wrapper-lf > div.houseInfoBox > div > div.houseInfo-wrap > ul > li:nth-child(10) > div.houseInfo-content::text').extract_first()
        release_date = response.css(
            '#content > div.wrapper > div.wrapper-lf > div.houseInfoBox > div > div.houseInfo-wrap > ul > li:nth-child(7) > div.houseInfo-content::text').extract_first()
        item['release_date'] = re.sub(r'\n|\t', '', release_date).replace('年','')
        item['image_urls'] = response.css(
            'div.img_wrap img::attr(src)').extract()
        item['from_url'] = response.url
        item['house_structure'] = response.css(
            '#introduction div.base ul > li:nth-child(8)::text').extract_first()
        yield item
