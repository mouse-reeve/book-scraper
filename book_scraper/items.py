import scrapy

class BookItem(scrapy.Item):
    name = scrapy.Field()
    year = scrapy.Field()
    isbn = scrapy.Field()
