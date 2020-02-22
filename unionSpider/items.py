# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class UnionItem(scrapy.Item):
    title = scrapy.Field()
    price = scrapy.Field()
    unit_price = scrapy.Field()
    # 小区名字
    community_name = scrapy.Field()
    # 地区,位置
    region = scrapy.Field()
    # 户型
    type = scrapy.Field()
    # 建筑面积
    construction_area = scrapy.Field()
    # 房屋朝向
    orientation = scrapy.Field()
    # 装修情况
    decoration = scrapy.Field()
    # 所在楼层
    floor = scrapy.Field()
    # 电梯
    elevator = scrapy.Field()
    # 房屋用途 房屋类型
    purposes = scrapy.Field()
    # 挂牌时间 建造年代
    release_date = scrapy.Field()
    image_urls = scrapy.Field()
    from_url = scrapy.Field()
    house_structure = scrapy.Field()
