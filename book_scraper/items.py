import scrapy

class BookItem(scrapy.Item):
    isbn = scrapy.Field()
    year = scrapy.Field()
    characters = scrapy.Field()
    places = scrapy.Field()
    purchasedAt = scrapy.Field()
