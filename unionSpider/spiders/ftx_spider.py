# -*- coding: utf-8 -*-
import scrapy
import re

from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

from unionSpider.items import UnionItem

class FangSpider(scrapy.Spider):
    name = 'ftx'
    allowed_domains = ['fang.com']
    start_urls = ['https://cd.esf.fang.com/']

    rules = {
        # 房产详情链接
        Rule(LinkExtractor(
            restrict_xpaths="//div[contains(@class,'shop_list')]/dl//h4[@class='clearfix']/a"),
            follow=True, callback="process_item"),
        # 翻页链接
        Rule(LinkExtractor(
            restrict_xpaths="//div[@class='page_al']/p/a"), follow=True),
    }

    def parse(self,response):
        dls = response.xpath("//div[contains(@class,'shop_list')]/dl")
        for dl in dls:
            item = UnionItem()
            name = dl.xpath(".//h4[@class='clearfix']/a/span/text()").get()
            infos = dl.xpath(".//p[@class='tel_shop']/text()").getall()
            infos = list(map(lambda x:re.sub(r'\s','',x),infos))
            for info in infos:
                if '厅' in info:
                    item['rooms'] = info
                elif '层' in info:
                    item['floor'] = info
                elif '向' in info:
                    item['toward'] = info
                elif '㎡' in info:
                    item['area'] = info
                elif '年' in info:
                    item['year'] = info
            address = dl.xpath(".//p[@class='add_shop']/span/text()").get()
            item['address'] = address
            price = ''.join(dl.xpath(".//span[@class='red']//text()").getall())
            item['price'] = price
            unit = dl.xpath(".//dd[@class='price_right']/span[not(@class)]/text()").get()
            item['unit'] = unit

            item['origin_url'] = response.urljoin(dl.xpath(".//h4[@class='clearfix']/a/@href").get())

            yield item

        next_url = response.xpath("//div[@class='page_al']/p/a/@href").get()
        if next_url:
            yield scrapy.Request(response.urljoin(next_url),callback=self.parse_esfhouse(),meta={"info":(province,city)})
