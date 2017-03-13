# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

"""
import pymongo

from .spiders.zlzp import ZlzpSpider
from .spiders.wyjob import WyjobSpider
from .spiders.zbtong import ZbtongSpider
from .spiders.neitui import NeituiSpider

from .items import SpecItem,NewsItem,ZpItem

class TutorialsPipeline(object):
    def process_item(self, item, spider):
        return item

class MongoPipeline(object):
    collection_name = 'scrapy_ershoufang_items'
    collection_name1 = 'scrapy_cj_ershoufang_items'
    zp_collection_name = 'zp_info_table'
    oly_collection_name = 'aoyun_news_table'
    oly_spec_collection = 'aoyun_spec_table'

    def __init__(self,mongo_uri,mongo_db):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db


    @classmethod
    def from_crawler(cls,crawler):
        return cls(
            mongo_uri = crawler.settings.get('MONGO_URI'),
            mongo_db = crawler.settings.get('MONGO_DATABASE','items')
        )

    def open_spider(self,spider):
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]

    def close_spider(self,spider):
        self.client.close()

    def process_item(self,item,spider):
        if isinstance(item,SpecItem):
            self.db[self.oly_spec_collection].insert(dict(item))
        elif isinstance(item,NewsItem):
            key_index = item['url']
            if not self.db[self.oly_collection_name].find({'url':key_index}).count():
                self.db[self.oly_collection_name].insert(dict(item))
        else:
            key_index = item['url']
            if not self.db[self.zp_collection_name].find({'url':key_index}).count():
                self.db[self.zp_collection_name].insert(dict(item))
        return item

"""        
        
import json
import codecs

class JsonWithEncodingPipeline(object):

    def __init__(self):
        self.file = codecs.open('data_utf8.json', 'w', encoding='utf-8')

    def process_item(self, item, spider):
        line = json.dumps(dict(item), ensure_ascii=False) + "\n"
        self.file.write(line)
        return item

    def close_spider(self, spider):
        self.file.close()



import MySQLdb
from datetime import datetime
import re


class MySQLStoreCnblogsPipeline(object):

    def __init__(self):
        self._conn=MySQLdb.connect(host="localhost",user="scrapy",passwd="scrapy",db="scrapy",charset="utf8")
        self._cur=self._conn.cursor()
        self._cur.execute("truncate table tj")

    # pipeline默认调用
    def process_item(self, item, spider):

    # 将每行更新或写入数据库中
        now = datetime.now().replace(microsecond=0).isoformat(' ')
        unitp = re.findall(r'\d+\.?\d*',item['unit_price'][0])
#        print("i am begin %s \n" %unitp)
        try:
            self._cur.execute("""
              insert into tj (name ,total_price, unit_price, title,  updated)
              values(%s,%s, %s, %s, %s)
              """, ( item['name'][0], item['total_price'][0], unitp[0], item['title'][0], now))

            isUpdate=self._cur.execute("select * from result where TO_DAYS(NOW()) - TO_DAYS(updated) = 0")
#            print(isUpdate)
            if isUpdate == 0 :
                self._cur.execute("""
                  insert into tj_h (name ,total_price, unit_price, title,  updated)
                  values(%s,%s, %s, %s, %s)
                  """, ( item['name'][0], item['total_price'][0], unitp[0], item['title'][0], now))

            self._conn.commit()
        except MySQLdb.Error, e:
            print "Error %d: %s" % (e.args[0], e.args[1])
        return item


    def __del__(self):
        u'释放资源（系统GC自动调用）'
#        print "i am end \n"
        self.caculate()
        try:
            self._cur.close()
            self._conn.close()
        except:
            pass


    def close(self):
        u'关闭数据库连接'
        self.__del__()


    def caculate(self):

        now = datetime.now().replace(microsecond=0).isoformat(' ')

        try:

            self._cur.execute("select DISTINCT name from tj ")
            allName = self._cur.fetchall()

            for oneName in allName :
                MyName = oneName[0]
#                print(MyName)
                self._cur.execute("""select floor(avg(unit_price)) from tj
                            where name = %s; """ ,MyName )
                average = self._cur.fetchone()

                number = self._cur.execute("""select * from tj
                            where name = %s; """ ,MyName )

#                print(number)
                self._cur.execute("""select min(unit_price) from tj
                            where name = %s; """ ,MyName )
                min = self._cur.fetchone()


#                print(min)
                isValue=self._cur.execute(""" select average,number from result WHERE TO_DAYS(NOW()) - TO_DAYS(updated) = 1
                                  AND name = %s; """ ,MyName )
                if isValue:
                    yestodayAverage = self._cur.fetchone()
                    increase = (float(average[0]) - float(yestodayAverage[0]))/float(yestodayAverage[0])
                    incNum = int(number) - int(yestodayAverage[1])
                else:
                    increase = 0
                    incNum = 0

#                print(increase)
                isUpdate=self._cur.execute("""select * from result where TO_DAYS(NOW()) - TO_DAYS(updated) = 0
                            AND name = %s; """ ,MyName )

#                print(isUpdate)
                if isUpdate:
                    self._cur.execute("""
                      update result set  number = %s ,incNum = %s ,average = %s ,min =%s, increase = %s , updated = %s
                      where TO_DAYS(NOW()) - TO_DAYS(updated) = 0
                      AND name = %s; """
                      , ( number,incNum,average[0],min[0], increase, now,MyName))
#                    print("i am update %s" %MyName)
                else:
                    self._cur.execute("""
                      insert into result ( name,number,incNum,average,min, increase,updated)
                      values(%s,%s,%s,%s,%s,%s,%s)
                      """, (  MyName ,number,incNum,average[0],min[0], increase, now))
#                    print("i am insert %s" %MyName)

                print("%s   %s  %s  %s  %s  %.2f%%"%(MyName,number,incNum,average[0],min[0],increase*100 ))

                self._conn.commit()

            print("\n\n")

            self._cur.execute("select *  from result where increase != 0 or incNum != 0")
            allLine = self._cur.fetchall()
            for oneLine in allLine :
                print("%s   %s  %s  %s  %s  %.2f%%" \
                     %(oneLine[1],oneLine[2],oneLine[3],\
                       oneLine[4],oneLine[5],oneLine[6]*100))

        except MySQLdb.Error, e:
            print "Error %d: %s" % (e.args[0], e.args[1])


        pass



from scrapy.exceptions import DropItem

class DuplicatesPipeline(object):

    def __init__(self):
        self.ids_seen = set() #注意到set型数据的应用

    def process_item(self, item, spider):
        judgeStr =item['name'][0] + item['total_price'][0] + item['unit_price'][0] + item['title'][0]

        if judgeStr in self.ids_seen:
            raise DropItem("Duplicate item found: %s" % item)
        else:
            self.ids_seen.add(judgeStr)
            return item


