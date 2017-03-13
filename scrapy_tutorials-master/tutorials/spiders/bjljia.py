# -*- coding: utf-8 -*-
import scrapy

from scrapy.spider import CrawlSpider,Rule
from scrapy.linkextractors import LinkExtractor
from ..items import CjHouseItem

class BjljiaSpider(CrawlSpider):
    name = "bjljia"
    allowed_domains = ["hf.lianjia.com",\
                       "tj.lianjia.com", \
                       "hz.lianjia.com",\
                       ]

#       starurlStr(self,'tj','jiahaihuayuan',2)
    def startUrlStr(city,house,pageNum):
        urlList = []
        i = 0
        while i < pageNum :
            i = i + 1
            urlStr = 'http://'
            urlStr = urlStr + city + '.lianjia.com/ershoufang/pg' + str(i) + 'rs' + house + '/'
            urlList.append(urlStr)
        return urlList

#       ruleStr('jiahaihuayuan',2)
    def ruleStr(house,pageNum):
        ruleList = []
        i = 0
        while i < pageNum :
            i = i + 1
            tmpStr = 'ershoufang/'
            tmpStr = tmpStr + 'pg' + str(i) + 'rs' + house + '/'
            ruleList.append(Rule(LinkExtractor(allow= tmpStr,),callback='parse_pg_chengjiao_house_info',follow=True) )
        return ruleList

####################################important####################################
    start_urls = \
                startUrlStr('tj','renhenghaiheguangchang',2) + \
                 startUrlStr('tj','jiahaihuayuan',1) + \
                 startUrlStr('tj','beianhuating',1) + \
                 startUrlStr('tj','jingdehuayuan',1) + \
                 startUrlStr('hf','shijichengzhenhuiyuan',2) + \
                 startUrlStr('hf','yinxiangxihu',3)

    rules = \
            ruleStr('renhenghaiheguangchang',2) + \
            ruleStr('jiahaihuayuan',1) + \
            ruleStr('beianhuating',1) + \
            ruleStr('jingdehuayuan',1) + \
            ruleStr('shijichengzhenhuiyuan',2) + \
            ruleStr('yinxiangxihu',3)


    
    def parse_pg_chengjiao_house_info(self,response):
        lists = response.css('ul[class="sellListContent"] li')
        items = []
        for index,list in enumerate(lists):
            item = CjHouseItem()
#            item['page_url'] = list.css("a[class='img']::attr(href)").extract()
            item['name'] = list.css("div[class='houseInfo'] a::text").extract()
            item['title'] = list.css("div[class='houseInfo']::text").extract()
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



