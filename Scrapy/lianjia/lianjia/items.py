# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy

class HouseItem(scrapy.Item):
    # define the fields for your item here like:
    _id = scrapy.Field()
    house_id = scrapy.Field()       #链家编号
    community_id = scrapy.Field()   #小区id
    community_name = scrapy.Field()   #小区name
    href = scrapy.Field()        #房源链接
    region = scrapy.Field()      #行政区域
    name = scrapy.Field()        #房源名称
    style = scrapy.Field()       #房源结构
    built_up_area = scrapy.Field()    #建筑面积
    inner_area = scrapy.Field()    #套内面积
    orientation = scrapy.Field()    #朝向
    decoration = scrapy.Field()     #装修
    property_right_age_limit = scrapy.Field()     #产权年限
    elevator = scrapy.Field()       #电梯
    floor = scrapy.Field()          #楼层高度
    list_time = scrapy.Field()      #挂牌时间
    last_sign_time = scrapy.Field()      #上次签约时间
    transaction_type = scrapy.Field()      #交易权属
    house_type = scrapy.Field()      #房产用途
    tax = scrapy.Field()       #税费

class CommunityItem(scrapy.Item):
    _id = scrapy.Field()
    community_id = scrapy.Field()   #小区id
    community = scrapy.Field()   #小区名称
    build_year = scrapy.Field()     #建造时间
    total_households = scrapy.Field()    #总户数
    house_property = scrapy.Field()      #物业
    developer = scrapy.Field()      #开发商
    property_fee = scrapy.Field()   #物业费

class HousePriceItem(scrapy.Item):
    _id = scrapy.Field()
    house_id = scrapy.Field()       #链家编号
    community_id = scrapy.Field()   #小区id
    community = scrapy.Field()   #小区名称
    capture_time = scrapy.Field()   #截获时间
    unit_price = scrapy.Field()     #每平米单价
    total_price = scrapy.Field()    #总价
    follow_total = scrapy.Field()   #总关注
    view_total = scrapy.Field()     #总带看

class TransactionItem(scrapy.Item):
    _id = scrapy.Field()
    house_id = scrapy.Field()       #链家编号
    community_id = scrapy.Field()   #小区id
    community = scrapy.Field()   #小区名称
    transaction_price = scrapy.Field()  #成交总价
    transaction_unit_price = scrapy.Field()     #成交单价
    list_price = scrapy.Field()     #挂牌价
    follow_total = scrapy.Field()   #总关注
    view_total = scrapy.Field()     #总带看
    transaction_period = scrapy.Field()     #成交周期
    transaction_date = scrapy.Field()       #成交日期

class HistroyTransactionItem(scrapy.Item):
    _id = scrapy.Field()
    house_id = scrapy.Field()   #链家编号
    transaction_date = scrapy.Field()       #成交日期
    transaction_price = scrapy.Field()  #成交总价







