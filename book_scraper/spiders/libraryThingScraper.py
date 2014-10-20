import scrapy
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors import LinkExtractor
from book_scraper.items import BookItem

isbns = ['9780099479314', '9780679745587']

class LibraryThingSpider(scrapy.Spider):
    name = 'LibraryThing'
    allowed_domains = ['librarything.com']
    start_urls = [];
    for isbn in isbns:
        start_urls.append('http://www.librarything.com/isbn/' + isbn)
    rules = [Rule(LinkExtractor(allow=['/commonknowledge/\d+']), 'parse')]

    def parse(self, response):
        if not 'commonknowledge' in response.url:
            pass

        item = BookItem()
        table = response.xpath('//div[@id="fwikiContainerTablediv"]//tr')
        for row in table:
            rowData = row.extract()
            if 'Original publication date' in rowData:
                item['year'] = row.xpath('.//a/text()').extract()[0]
        item['isbn'] = self.isbn

        yield item


