# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import pymysql
import datetime
from twisted.internet.error import TCPTimedOutError, TimeoutError


class Spider3Pipeline:
    def __init__(self):
        self.connect = pymysql.connect(host='localhost',
                                       user='root',
                                       password='159753',
                                       db='web_novel',
                                       port=3306,
                                       charset="utf8mb4")
        self.cursor = self.connect.cursor()

    def process_exception(self, request, exception, spider):
        if isinstance(exception, TimeoutError):
            return request
        elif isinstance(exception, TCPTimedOutError):
            return request

    def process_item(self, item, spider):
        novel_name = item["novel_name"]
        novel_name = novel_name.replace('"', '').replace("'", "")
        author = item['author']
        author = author.replace('"', '').replace("'", "")
        format = '%Y-%m-%d %H:%M:%S'
        nowTime = datetime.datetime.now().strftime(format)  # 将datetime转换为字符串
        domain = item['domain']
        download_url = item['download_url']
        sql = """ INSERT INTO allNovel2(novel_name,author,date,domain,download_url)
                  SELECT "%s", "%s", "%s", "%s", "%s" 
                  FROM DUAL
                  WHERE NOT EXISTS
                  (SELECT * FROM allNovel2 WHERE novel_name = "%s" AND author = "%s")""" \
              % (novel_name, author, nowTime, domain, download_url, novel_name, author)
        self.cursor.execute(sql)
        self.connect.commit()

    def close_spider(self, spider):
        self.cursor.close()
        self.connect.close()
