# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import csv
import pymysql.cursors
from pymongo import MongoClient
import traceback
from scrapy.exceptions import DropItem


class CSVPipeline(object):
    file = None

    def open_spider(self, spider):
        self.file = open("E:\\Graduation Project\\DataAnalysis\\data\\total_house.csv", "a" ,newline='')

    def process_item(self, item, spider):
        self.writer = csv.writer(self.file)
        self.writer.writerow((item['title'], item['price'], item['unit_price'], item['community_name'],
                                        item['region'], item['type'], item['construction_area'], item['orientation'],
                                        item['decoration'],item['floor'],item['elevator'],item['purposes'],item['release_date'],
                                        item['house_structure'],item['image_urls'],item['from_url']))
        return item

    def close_spider(self, spider):
        self.file.close()
