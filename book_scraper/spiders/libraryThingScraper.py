import scrapy
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors import LinkExtractor
from book_scraper.items import BookItem

isbns = ['9780099479314', '9780679745587', '0061059064']

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
        item['isbn'] = self.isbn

        table = response.xpath('//div[@id="fwikiContainerTablediv"]//tr')
        for row in table:
            rowData = row.extract()
            if 'Original publication date' in rowData:
                item['year'] = row.xpath('.//a/text()').extract()[0]
            elif 'Important places' in rowData:
                item['places'] = row.xpath('.//a/text()').extract()
            elif 'People/Characters' in rowData:
                item['characters'] = row.xpath('.//a/text()').extract()

        yield item

