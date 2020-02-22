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

    def parse(self, response):
        next_url = response.urljoin(response.xpath("//div[@class='page_al']/p/a/@href").extract_first())
        print('*********' + str(next_url) + '**********')
        # if next_url:
        #     yield scrapy.Request(url=next_url,callback=self.parse)

        dls = response.xpath("//div[contains(@class,'shop_list')]/dl")[:1]
        for dl in dls:
            url = response.urljoin(dl.xpath(".//h4[@class='clearfix']/a/@href").extract_first())
            yield scrapy.Request(url, callback=self.parse_detail)

    def parse_detail(self,response):
        item = UnionItem()
        item['title'] = response.css('#lpname > h1 > span::text').extract_first()
        item['price'] = response.css(
            'div.tab-cont.clearfix > div.tab-cont-right > div.tr-line.clearfix.zf_new_title > div.trl-item_top > div.trl-item.price_esf.sty1 > i::text').extract_first()
        item['unit_price'] = response.css(
            'div.tab-cont.clearfix > div.tab-cont-right > div:nth-child(2) > div.trl-item1.w132 > div.tt::text').extract_first()
        community_name_pre = response.css(
            'div.tab-cont.clearfix > div.tab-cont-right > div:nth-child(4) > div:nth-child(1) > div.rcont::text').extract_first()
        community_name_end = response.css(
            'div.tab-cont.clearfix > div.tab-cont-right > div:nth-child(4) > div:nth-child(1) > div.rcont > span::text').extract_first()
        if community_name_pre and community_name_end:
            item['community_name'] = community_name_pre + community_name_end
        else:
            item['community_name'] = community_name_pre
        regin_pre = response.css(
            '#kesfsfbxq_C03_07::text').extract_first()
        regin_end = response.css(
            '#kesfsfbxq_C03_08::text').extract_first()
        if regin_pre and regin_end:
            item['region'] = regin_pre + regin_end
        else:
            item['region'] = regin_pre
        type = response.css(
            'div.tab-cont.clearfix > div.tab-cont-right > div:nth-child(2) > div.trl-item1.w146 > div.tt::text').extract_first()
        # item['type'] = re.sub(r'\r|\t','',type)
        item['type'] = type
        item['construction_area'] = response.css(
            'div.tab-cont.clearfix > div.tab-cont-right > div:nth-child(2) > div.trl-item1.w182 > div.tt::text').extract_first()
        item['orientation'] = response.css(
            'div.tab-cont.clearfix > div.tab-cont-right > div:nth-child(3) > div.trl-item1.w146 > div.tt::text').extract_first()
        item['decoration'] = response.css(
            'div.tab-cont.clearfix > div.tab-cont-right > div:nth-child(3) > div.trl-item1.w132 > div.tt::text').extract_first()
        item['floor'] = response.css(
            'div.tab-cont.clearfix > div.tab-cont-right > div:nth-child(3) > div.trl-item1.w182 > div.tt::text').extract_first()
        item['elevator'] = response.css(
            'div.w1200.clearfix > div.zf_new_left.floatl > div.content-item.fydes-item > div.cont.clearfix > div:nth-child(2) > span.rcont::text').extract_first()
        item['purposes'] = response.css(
            'div.w1200.clearfix > div.zf_new_left.floatl > div.content-item.fydes-item > div.cont.clearfix > div:nth-child(5) > span.rcont::text').extract_first()
        item['release_date'] = response.css(
            'div.w1200.clearfix > div.zf_new_left.floatl > div.content-item.fydes-item > div.cont.clearfix > div:nth-child(1) > span.rcont::text').extract_first()
        item['image_urls'] = response.css(
            '#bigImgBox > div.lbimg.lbcom.item.cur > img::attr(src)').extract()
        item['from_url'] = response.url
        item['house_structure'] = response.css(
            'div.w1200.clearfix > div.zf_new_left.floatl > div.content-item.fydes-item > div.cont.clearfix > div:nth-child(6) > span.rcont::text').extract_first()
        yield item