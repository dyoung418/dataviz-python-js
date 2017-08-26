import scrapy
import re

'''This creates a 'nwinners_list' spider accessible from the main
scrapy folder for this project.  To run it, go to that folder and
type 'scrapy crawl nwinners_list -o nobel_winners.json'.

You can see all the spiders available to run with 'scrapy list'
'''

# A. Define the data to be scraped

class SimpleNWinnerItem(scrapy.Item):
    country = scrapy.Field()
    name = scrapy.Field()
    link_text = scrapy.Field()

# B. Create a named spider

class SimpleNWinnerSpider(scrapy.Spider):
    '''Scrapes the country and link text of Nobel winners'''
    name = 'simple_nwinners_list'
    allowed_domains = ['en-wikipedia.org']
    start_urls = [
        'https://en.wikipedia.org/wiki/List_of_Nobel_laureates_by_country' ]

    # C. a parse method to deal with the HTTP response
    def parse(self, response):
        h2s = response.xpath('//h2')
        for h2 in h2s:
            country = h2.xpath('span[@class="mw-headline"]/text()').extract()
            if country:
                winners = h2.xpath('following-sibling::ol[1]')
                for w in winners.xpath('li'):
                    #When this was the simpler version, it ended as follows:
                    text = w.xpath('descendant-or-self::text()').extract()
                    yield SimpleNWinnerItem(country=country[0],
                                     name=text[0],
                                     link_text=' '.join(text))
