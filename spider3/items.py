# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class BookItem(scrapy.Item):
    novel_name = scrapy.Field()
    author = scrapy.Field()
    date = scrapy.Field()
    domain = scrapy.Field()
    download_url = scrapy.Field()