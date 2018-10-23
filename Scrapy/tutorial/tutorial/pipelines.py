# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import psycopg2

class Stock_Info_Pipeline(object):
    def __init__(self):
        self.stock_items = []

    def process_item(self, item, spider):
        self.stock_items.append(item)
        if len(self.stock_items) >= 1000:
            conn = psycopg2.connect(database="StockDatas", user="postgres", password="123569", host="127.0.0.1", port="5432")
            cur = conn.cursor()
            for item in self.stock_items:
                try:
                    cur.execute("INSERT INTO \"StockInfo\" (stock_code, stock_name) VALUES(%s, %s);",
                    (item['stock_code'],item['stock_name']) )
                except Exception as e :
                    print('insert record into table failed')
                    print(e)
            conn.commit()
            if cur:
                cur.close()
                conn.close()
            self.stock_items = []
        return item

    def close_spider(self, spider):
        conn = psycopg2.connect(database="StockDatas", user="postgres", password="123569", host="127.0.0.1", port="5432")
        cur = conn.cursor()
        for item in self.stock_items:
            try:
                cur.execute("INSERT INTO \"StockInfo\" (stock_code, stock_name) VALUES(%s, %s);",
                (item['stock_code'],item['stock_name']) )
            except Exception as e :
                print('insert record into table failed')
                print(e)
        conn.commit()
        if cur:
            cur.close()
            conn.close()        


class TutorialPipeline(object):
    def __init__(self):
        self.stock_items = []

    def process_item(self, item, spider):
        self.stock_items.append(item)
        if len(self.stock_items) >= 5000:
            conn = psycopg2.connect(database="StockDatas", user="postgres", password="123569", host="127.0.0.1", port="5432")
            cur = conn.cursor()
            for item in self.stock_items:
                try:
                    cur.execute("INSERT INTO \"StockDateLine\" (stock_code, value_date, start_value, end_value, max_value, min_value, volume, turn_volume) VALUES(%s, %s, %s, %s, %s, %s, %s, %s);",
                    (item['stock_code'],item['date'],item['start_value'],item['end_value'],item['max_value'],item['min_value'],item['volume'],item['turn_volume']) )
                except Exception as e :
                    print('insert record into table failed')
                    print(e)
            conn.commit()
            if cur:
                cur.close()
                conn.close()
            self.stock_items = []
        return item

    
