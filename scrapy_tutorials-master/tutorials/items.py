# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class CjHouseItem(scrapy.Item):
    name = scrapy.Field() #小区
    title = scrapy.Field() #信息
    total_price = scrapy.Field() #总价
    unit_price = scrapy.Field() #单价
    url = scrapy.Field() #单价



