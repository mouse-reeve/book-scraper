import re
import csv
import scrapy
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors import LinkExtractor
from book_scraper.items import BookItem

class LibraryThingSpider(scrapy.Spider):
    name = 'LibraryThing'
    allowed_domains = ['librarything.com']
    start_urls = [];

    start_urls.append('https://www.librarything.com/catalog_bottom.php?view=tripofmice')

    # this does not seem to be working AT ALL
    rules = [
        #Rule(LinkExtractor(allow=['offset=\d+']), 'parse'),
        Rule(LinkExtractor(allow=['/book/\d+']), 'parse'),
        Rule(LinkExtractor(allow=['/commonknowledge/\d+']), 'parse')
    ]

    def parse(self, response):
        for link in response.xpath('//a/@href'):
            path = link.extract()
            if re.match('\/work\/\d+\/book\/\d+', path):
                yield scrapy.http.Request('https://www.librarything.com/' + path)

        item = BookItem()

        try:
            item['isbn'] = response.xpath('//meta[@property="books:isbn"]/@content').extract()[0]
        except:
            pass

        table = response.xpath('//div[@id="fwikiContainerTablediv"]//tr')
        for row in table:
            rowData = row.extract()
            if 'Original publication date' in rowData:
                print row.xpath('.//a/text()').extract()
                try:
                    item['year'] = row.xpath('.//a/text()').extract()[0]
                except:
                    # maybe not ideal error handling here?
                    pass
            elif 'Important places' in rowData:
                item['places'] = row.xpath('.//a/text()').extract()
            elif 'People/Characters' in rowData:
                item['characters'] = row.xpath('.//a/text()').extract()

        yield item

