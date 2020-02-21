# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html


import re
from scrapy.exceptions import DropItem
import csv


class LianjiaFilterPipeline(object):

    def process_item(self, item, spider):
        item['area'] = re.findall(r"\d+\.?\d*", item["area"])[0]
        if item["direction"] == '暂无数据':
            raise DropItem("房屋朝向无数据，抛弃此项目：%s" % item)
        return item


class LianjiaCSVPipeline(object):
    index = 0
    file = None

    def open_spider(self, spider):
        self.file = open("house.csv", "a")

    def process_item(self, item, spider):
        if self.index == 0:
            column_name = "name,room_type,area,direction,fitment,elevator,total_price,unit_price,property_right\n"
            self.file.write(column_name)
            self.index = 1
        self.writer = csv.writer(self.file)
        self.writer.writerow((item['name'], item['room_type'], item['area'], item['direction'], item[
                             'fitment'], item['elevator'], item['total_price'], item['unit_price'], item['property_right']))
        return item

    def close_spider(self, spider):
        self.file.close()
