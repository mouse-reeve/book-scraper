import re
import scrapy
from book_scraper.items import BookItem

class LibraryThingSpider(scrapy.Spider):
    name = 'LibraryThing'
    allowed_domains = ['librarything.com']
    start_urls = ['https://www.librarything.com/catalog_bottom.php?view=tripofmice']

    def parse(self, response):
        for link in response.xpath('//a/@href'):
            path = link.extract()
            if re.match('\/work\/\d+\/book\/\d+', path)\
                    or re.match('\/catalog_bottom.php\?view\=tripofmice\&offset=\d+', path)\
                    or re.match('\/work\/\d+\/details\/\d+', path):
                yield scrapy.http.Request('https://www.librarything.com/' + path)

        item = BookItem()

        try:
            item['isbn'] = response.xpath('//meta[@property="books:isbn"]/@content').extract()[0]
        except:
            pass

        # About page (with common knowledge)
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
                    pass

            elif 'Important places' in rowData:
                item['places'] = row.xpath('.//div[@class="fwikiAtomicValue"]//a/text()').extract()

            elif 'People/Characters' in rowData:
                item['characters'] = row.xpath('.//div[@class="fwikiAtomicValue"]//a/text()').extract()

            elif 'Important events' in rowData:
                item['events'] = row.xpath('.//div[@class="fwikiAtomicValue"]//a/text()').extract()

        # Details page
        table = response.xpath('//table[@id="book_bookInformationTable"]//tr')
        for row in table:
            rowData = row.extract()
            if 'From where' in rowData:
                store = row.xpath('.//div[@class="xlocation"]//a/text()').extract()
                if store:
                    item['purchasedAt'] = store

            if 'Tags' in rowData:
                tags = row.xpath('.//td[@class="bookeditfield"]//a/text()').extract()
                if tags:
                    item['tags'] = tags

        if item:
            yield item

