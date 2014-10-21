import csv
import scrapy
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors import LinkExtractor
from book_scraper.items import BookItem

class LibraryThingSpider(scrapy.Spider):
    name = 'LibraryThing'
    allowed_domains = ['librarything.com']
    start_urls = [];

    # I should generalize this
    fileName = 'library.csv'

    with open(fileName, 'rb') as f:
        reader = csv.DictReader(f)
        for row in reader:
            if 'isbn' in row:
                isbn = row['isbn']
                start_urls.append('http://www.librarything.com/isbn/' + isbn)
            else:
                continue

    rules = [
        Rule(LinkExtractor(allow=['/commonknowledge/\d+']), 'parse')
    ]

    def parse(self, response):
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


