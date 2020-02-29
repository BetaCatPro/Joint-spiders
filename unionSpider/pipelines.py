# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html


import re
import csv


class CSVPipeline(object):
    index = 0
    file = None

    def open_spider(self, spider):
        # self.file = open("E:\\毕设\\DataAnalysis\\data\\tianfuxinqunanqu_house.csv", "a" ,encoding='utf-8',newline='')
        self.file = open("E:\\Graduation Project\\DataAnalysis\\data\\xindu_house.csv", "a",newline='')

    def process_item(self, item, spider):
        if self.index == 0:
            column_name = "title,price,unit_price,community_name,region,type,construction_area,orientation,decoration,floor,elevator,purposes,release_date,house_structure,image_urls,from_url\n"
            self.file.write(column_name)
            self.index = 1
        self.writer = csv.writer(self.file)
        self.writer.writerow((item['title'], item['price'], item['unit_price'], item['community_name'],
                                        item['region'], item['type'], item['construction_area'], item['orientation'],
                                        item['decoration'],item['floor'],item['elevator'],item['purposes'],item['release_date'],
                                        item['house_structure'],item['image_urls'],item['from_url']))
        return item

    def close_spider(self, spider):
        self.file.close()

class TestPipeline(object):
    file = None

    def open_spider(self, spider):
        # 多个爬虫salve同时写入同一house.csv
        self.file = open("house.csv", "a",newline='')

    def process_item(self, item, spider):
        self.writer = csv.writer(self.file)
        self.writer.writerow((item['title'], item['price'], item['unit_price'], item['community_name'],
                                        item['region'], item['type'], item['construction_area'], item['orientation'],
                                        item['decoration'],item['floor'],item['elevator'],item['purposes'],item['release_date'],
                                        item['house_structure'],item['image_urls'],item['from_url']))
        return item

    def close_spider(self, spider):
        self.file.close()
