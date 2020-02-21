# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class LianjiaItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    # 标题
    title = scrapy.Field()
    # 价格
    price = scrapy.Field()
    # 单价
    unit_price = scrapy.Field()
    # 小区名字
    community_name = scrapy.Field()
    # 地区
    region = scrapy.Field()
    # 联系人
    linkman = scrapy.Field()
    # 联系电话
    linktel = scrapy.Field()
    # 户型
    type = scrapy.Field()
    # 建筑面积
    construction_area = scrapy.Field()
    # 实际面积
    actual_area = scrapy.Field()
    # 房屋朝向
    orientation = scrapy.Field()
    # 装修情况
    decoration = scrapy.Field()
    # 所在楼层
    floor = scrapy.Field()
    # 电梯
    elevator = scrapy.Field()
    # 产权年限
    property = scrapy.Field()
    # 房屋年限
    house_years = scrapy.Field()
    # 有无抵押
    mortgage = scrapy.Field()
    # 房屋用途
    purposes = scrapy.Field()
    # 挂牌时间
    release_date = scrapy.Field()
    # 房屋照片
    image_urls = scrapy.Field()
    # 房产链接
    from_url = scrapy.Field()


class AjkItem(scrapy.Item):
    code = scrapy.Field()
    name = scrapy.Field()
    parent_code = scrapy.Field()
    display_order = scrapy.Field()


class FtxItem(scrapy.Item):
    name = scrapy.Field()
    rooms = scrapy.Field()
    floor = scrapy.Field()
    toward = scrapy.Field()
    year = scrapy.Field()
    address = scrapy.Field()
    area = scrapy.Field()
    # 总价
    price = scrapy.Field()
    # 单价
    unit = scrapy.Field()
    origin_url = scrapy.Field()
