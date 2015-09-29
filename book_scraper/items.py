''' defines what data will be collected '''
import scrapy

class BookItem(scrapy.Item):
    ''' metadata about a book '''
    isbn = scrapy.Field()
    date_first_published = scrapy.Field()
    characters = scrapy.Field()
    places = scrapy.Field()
    events = scrapy.Field()
