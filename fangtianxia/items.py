# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class NewHouseItem(scrapy.Item):
    province = scrapy.Field() #省份
    city = scrapy.Field()     #城市
    name = scrapy.Field()     #小区名
    roows = scrapy.Field()
    price = scrapy.Field()    #价格
    area = scrapy.Field()     #面积
    address = scrapy.Field()  #地址
    district = scrapy.Field() #区域
    sale = scrapy.Field()     #是否在售
    origin_url = scrapy.Field() #页面详情

class EsfHouseItem(scrapy.Item):
    province = scrapy.Field() #省份
    city = scrapy.Field()     #城市
    name = scrapy.Field()     #小区名
    price = scrapy.Field()    #价格
    rooms = scrapy.Field()    #几房几厅
    floor = scrapy.Field()    #层
    area = scrapy.Field()     #面积
    address = scrapy.Field()  #地址
    year = scrapy.Field()     #年代
    unit = scrapy.Field()     #单价
    toward = scrapy.Field()   #朝向
    origin_url = scrapy.Field() #页面详情
