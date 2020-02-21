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
        self.file = open("home.csv", "a")

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

import pymysql
class AjkPipeline(object):

    def __init__(self):
        self.db = pymysql.connect(
            "localhost", "root", "123456", "house", charset="utf8")
        self.cursor = self.db.cursor()

    def __del__(self):
        self.db.close()

    def process_item(self, item, spider):
        select_sql = "select id from house_area where code='%s'" % item['code']
        already_save = self.cursor.execute(select_sql)
        self.db.commit()

        if already_save == 1:
            # 更新
            update_sql = "update house_area set name='%s' where code='%s'" % (
                item['name'], item['code'])
            self.cursor.execute(update_sql)
            self.db.commit()
        else:
            parent_id = 0

            # 查询父级区域
            if item['parent_code']:
                select_sql = "select id from house_area where code='%s'" % item[
                    'parent_code']
                already_save = self.cursor.execute(select_sql)
                house_area = self.cursor.fetchone()
                self.db.commit()

                if already_save == 1:
                    parent_id = house_area[0]

            # 插入
            insert_sql = "insert into house_area(code,name,parent_id,parent_code,display_order)\
                values('%s','%s','%d','%s','%d')"\
                % (item['code'], item['name'], parent_id, item['parent_code'], item['display_order'])
            self.cursor.execute(insert_sql)
            self.db.commit()
        return item


from scrapy.exporters import JsonLinesItemExporter

class FangtxPipeline(object):
    def __init__(self):
        self.newhouse_fp = open('newhouse.json','wb')
        self.esfhouse_fp = open('esfhouse.json', 'wb')
        self.newhouse_exporter = JsonLinesItemExporter(
            self.newhouse_fp,ensure_ascii=False
        )
        self.esfhouse_exporter = JsonLinesItemExporter(
            self.esfhouse_fp,ensure_ascii=False
        )

    def process_item(self, item, spider):
        self.newhouse_exporter.export_item(item)
        self.esfhouse_exporter.export_item(item)
        return item

    def close_spider(self):
        self.newhouse_fp.close()
        self.esfhouse_fp.close()
