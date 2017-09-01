import scrapy
import re
from scrapy.spidermiddlewares.httperror import HttpError
from twisted.internet.error import DNSLookupError
from twisted.internet.error import TimeoutError, TCPTimedOutError
import logging


'''This creates a 'quorum_basic' spider accessible from the main
scrapy folder for this project.  To run it, go to that folder and
type 'scrapy crawl quorum_basic -o qbasic.json'.

You can see all the spiders available to run with 'scrapy list'
'''

# A. Define the data to be scraped

class QBasicItem(scrapy.Item):
    name = scrapy.Field()
    link = scrapy.Field()
    positions = scrapy.Field()
    notes = scrapy.Field()
    born_in = scrapy.Field()
    date_of_birth = scrapy.Field()
    date_of_death = scrapy.Field()
    place_of_birth = scrapy.Field()
    place_of_death = scrapy.Field()
    apostle_not_quorum_member = scrapy.Field()
    section = scrapy.Field() #DEBUG

# B. Create a named spider

class QBasicSpider(scrapy.Spider):
    '''Scrapes the basic info of quorum of the twelve members'''
    name = 'basic_q12'
    allowed_domains = ['en-wikipedia.org']
    start_urls = [
        'https://en.wikipedia.org/wiki/List_of_members_of_the_Quorum_of_the_Twelve_Apostles_(LDS_Church)' ]

    # C. a parse method to deal with the HTTP response
    def parse(self, response):
        h2s = response.xpath('//h2')
        self.logger.debug('Parse: len(h2s) = %s', len(h2s))
        for h2 in h2s:
            sections = h2.xpath('span[@class="mw-headline"]')
            self.logger.debug('Parse: len(sections) = %s', len(sections))
            if sections:
                for section in sections:
                    section_text = h2.xpath('span[@class="mw-headline"]/text()').extract()[0]
                    if section_text in ['List notes']:
                        continue
                    table = h2.xpath('following-sibling::table[@class="wikitable"]')
                    self.logger.debug('Parse: section_text=%s len(table)=%s', section_text, len(sections))
                    if table:
                        table = table[0]
                        entries = table.xpath('tr[@class="vcard"]')
                        self.logger.debug('Parse: len(entries) = %s', len(entries))
                        for entry in entries:
                            qdata = {}
                            qdata['apostle_not_quorum_member'] = False
                            if section_text == 'Apostles who were never members of the Quorum of the Twelve':
                                qdata['apostle_not_quorum_member'] = True
                            qdata['name'] = entry.xpath(\
                                    'following-sibling::tr[1]/td[2]/p/span/a/text()').extract()[0]
                            qdata['link'] = entry.xpath(\
                                    'following-sibling::tr[1]/td[2]/p/span/a/@href').extract()[0]
                            qdata['section'] = section_text
                            qdata['date_of_birth'] = entry.xpath(\
                                    'following-sibling::tr[1]/td[2]/p/span[2]/span[@class="bday"]/text()').extract()[0]
                            yield QBasicItem(**qdata)



