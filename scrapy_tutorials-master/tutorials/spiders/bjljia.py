# -*- coding: utf-8 -*-
import scrapy

from scrapy.spider import CrawlSpider,Rule
from scrapy.linkextractors import LinkExtractor
from ..items import CjHouseItem

class BjljiaSpider(CrawlSpider):
    name = "bjljia"
    allowed_domains = ["tj.lianjia.com"]
    start_urls = (
#        'http://bj.lianjia.com/ershoufang/',
#        'http://bj.lianjia.com/chengjiao/',
#         'http://tj.lianjia.com/ershoufang/rsjiahaihuayuan/',
         'http://tj.lianjia.com/ershoufang/rsrenhenghaiheguangchang/',
         'http://tj.lianjia.com/ershoufang/pg2rsrenhenghaiheguangchang/',

    )

    rules = (
#        Rule(LinkExtractor(allow='ershoufang/[0-9]*\.html',),callback='parse_one_house_info',follow=True),
#        Rule(LinkExtractor(allow='ershoufang/rsjiahaihuayuan/[a-zA-Z0-9]*/',),callback='parse_pg_chengjiao_house_info',follow=True),
        Rule(LinkExtractor(allow='ershoufang/rsjiahaihuayuan/',),callback='parse_pg_chengjiao_house_info',follow=True),
        Rule(LinkExtractor(allow='ershoufang/rsrenhenghaiheguangchang/',),callback='parse_pg_chengjiao_house_info',follow=True),
        Rule(LinkExtractor(allow='ershoufang/pg2rsrenhenghaiheguangchang/',),callback='parse_pg_chengjiao_house_info',follow=False),
#        Rule(LinkExtractor(allow='ershoufang/[a-zA-Z0-9]*/',restrict_xpaths=('//div[@class="page-box house-lst-page-box"]'),),callback='parse_pg_chengjiao_house_info',follow=False),
#        Rule(LinkExtractor(allow='ershoufang/[a-zA-Z0-9]*/',),callback='parse_pg_chengjiao_house_info',follow=True),
#        Rule(LinkExtractor(allow='ershoufang/[0-9]*\.html',),callback='parse_chengjiao_house_info',follow=True),
#        Rule(LinkExtractor(allow='ershoufang',),follow=True),
#        Rule(LinkExtractor(allow='chengjiao/[a-zA-Z0-9]*/',),callback='parse_pg_chengjiao_house_info',follow=True),
#        Rule(LinkExtractor(allow='chengjiao/[a-zA-Z0-9]*\.html',),callback='parse_chengjiao_house_info',follow=True),
#        Rule(LinkExtractor(allow='chengjiao/[a-zA-Z0-9]*\.html',),callback='parse_one_house_info',follow=True),
#        Rule(LinkExtractor(allow='chengjiao',),follow=True),

    )


    
    def parse_pg_chengjiao_house_info(self,response):
        lists = response.css('ul[class="sellListContent"] li')
        items = []
        for index,list in enumerate(lists):
            item = CjHouseItem()
#            item['page_url'] = list.css("a[class='img']::attr(href)").extract()
            item['title'] = list.css("div[class='title'] a::text").extract()
#            item['house_info'] = list.css("div[class='houseInfo']::text").extract()
#            item['deal_data'] = list.css("div[class='dealDate']::text").extract()
            item['total_price'] = list.css("div[class='totalPrice'] span::text").extract()
#            item['position_icon'] =  list.css("div[class='positionInfo']::text").extract()
            item['unit_price'] = list.css("div[class='unitPrice'] span::text").extract()
#            item['deal_house_txt'] = list.css("div[class='dealHouseInfo'] span::text").extract()
#            item['sell_flag'] = 1
#            print type(item['total_price'])
#            print "haha\n"
            items.append(item)
        return items


