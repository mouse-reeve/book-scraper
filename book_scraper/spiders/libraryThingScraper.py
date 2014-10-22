import re
import scrapy
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors import LinkExtractor
from book_scraper.items import BookItem

class LibraryThingSpider(scrapy.Spider):
    name = 'LibraryThing'
    allowed_domains = ['librarything.com']
    start_urls = ['https://www.librarything.com/catalog_bottom.php?view=tripofmice']

    def parse(self, response):
        for link in response.xpath('//a/@href'):
            path = link.extract()
            if re.match('\/work\/\d+\/book\/\d+', path) or re.match('\/catalog_bottom.php\?view\=tripofmice\&offset=\d+', path):
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
                try:
                    year = row.xpath('.//a/text()').extract()[0]
                    # normalizes dates assuming the formats YYYY-MM-DD or
                    # YYYY-YY, both of which I've seen in the data.
                    year = year[0:4]
                    item['year']  = year
                except:
                    print '----YEAR ERROR----'
                    print row.xpath('.//a/text()').extract()
                    pass
            elif 'Important places' in rowData:
                item['places'] = row.xpath('.//div[@class="fwikiAtomicValue"]//a/text()').extract()
            elif 'People/Characters' in rowData:
                item['characters'] = row.xpath('.//div[@class="fwikiAtomicValue"]//a/text()').extract()

        if item:
            yield item

