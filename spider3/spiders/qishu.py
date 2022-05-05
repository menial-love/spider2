# -*- coding: utf-8 -*-
import scrapy
from spider3.items import BookItem

domain = "https://www.kankezw.com"

class QiShu(scrapy.Spider):
    name = 'qishu'
    start_urls = ['https://www.kankezw.com/']

    def parse(self, response, **kwargs):
        topics = response.xpath("//div[@class='nav']/a")[1:]
        for topic in topics:
            topic_url = domain + topic.xpath("./@href").extract()[0]
            yield scrapy.Request(url=topic_url, callback=self.getTopic)

    def getTopic(self, response):
        books = response.xpath("//div[@class='listBox']/ul/li/a")
        for book in books:
            book_url = domain + book.xpath("./@href").extract()[0]
            yield scrapy.Request(url=book_url, callback=self.getBook)

        page_control = response.xpath("//div[@class='tspage']/a")
        next_page_url = ""
        # 说明当前在第一页
        if len(page_control) == 2 and page_control[0].xpath("./text()").extract()[0] == '下一页':
            next_page_url = domain + page_control[0].xpath("./@href").extract()[0]
        # 说明当前在最后一页
        elif len(page_control) > 2:
            next_page_url = domain + page_control[2].xpath("./@href").extract()[0]
        # 翻页
        if next_page_url != "":
            yield scrapy.Request(url=next_page_url, callback=self.getTopic)

    def getBook(self, response):
        book_information = response.xpath("//div[@class='detail']/div[@class='detail_info']/div[@class='detail_right']")
        book_name_tmp = book_information.xpath("./h1/text()").extract()[0]
        index = book_name_tmp.find('》')
        book_name = "不知名书籍"
        try:
            book_name = book_name_tmp[1:index]
        except Exception as e:
            print(e)

        author = "佚名"
        try:
            author = book_information.xpath("./ul/li/text()")[5].extract().split("：")[1]
        except Exception as e:
            print(e)

        download_url = "javascript:void(0)"
        try:
            download_url = response.xpath("//div[@class='showDown']/ul/li[3]/script/text()").extract()[0].split(",")[1]
            download_url = download_url.replace("'", "")
        except Exception as e:
            print(e)

        item = BookItem()
        item['novel_name'] = book_name
        item['author'] = author
        item['domain'] = '奇书网'
        item['download_url'] = download_url
        yield item