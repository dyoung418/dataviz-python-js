import scrapy
import re
from scrapy.spidermiddlewares.httperror import HttpError
from twisted.internet.error import DNSLookupError
from twisted.internet.error import TimeoutError, TCPTimedOutError
import logging


'''This creates a 'nwinners_list' spider accessible from the main
scrapy folder for this project.  To run it, go to that folder and
type 'scrapy crawl nwinners_list -o nobel_winners.json'.

You can see all the spiders available to run with 'scrapy list'
'''

# A. Define the data to be scraped

class NWinnerItem(scrapy.Item):
    name = scrapy.Field()
    link = scrapy.Field()
    year = scrapy.Field()
    category = scrapy.Field()
    country = scrapy.Field()
    gender = scrapy.Field()
    born_in = scrapy.Field()
    date_of_birth = scrapy.Field()
    date_of_death = scrapy.Field()
    place_of_birth = scrapy.Field()
    place_of_death = scrapy.Field()
    text = scrapy.Field()

# B. Create a named spider

class NWinnerSpider(scrapy.Spider):
    '''Scrapes the country and link text of Nobel winners'''
    name = 'nwinners_list'
    allowed_domains = ['en-wikipedia.org']
    start_urls = [
        'https://en.wikipedia.org/wiki/List_of_Nobel_laureates_by_country' ]
    #download_delay = 2 # use this for error 999

#    def __init__(self, *args, **kwargs):
    ##    logger = logging.getLogger('scrapy.spidermiddlewares.httperror')
    ##    logger.setLevel(logging.WARNING)
    #    super().__init__(*args, **kwargs)
    #    self.logger.setLevel(logging.WARNING)

    # C. a parse method to deal with the HTTP response
    def parse(self, response):
        h2s = response.xpath('//h2')
        for h2 in h2s:
            country = h2.xpath('span[@class="mw-headline"]/text()').extract()
            if country:
                winners = h2.xpath('following-sibling::ol[1]')
                for w in winners.xpath('li'):
                    ''' #When this was the simpler version, it ended as follows:
                    text = w.xpath('descendant-or-self::text()').extract()
                    yield NWinnerItem(country=country[0],
                                     name=text[0],
                                     link_text=' '.join(text))
                    '''
                    wdata = self.process_winner_li(w, country[0])
                    # Follow link to bio page and scrape there
                    request = scrapy.Request(wdata['link'], 
                                        callback=self.parse_bio,
                                        errback = self.error_handler,
                                        dont_filter=True)
                    #give response access to NWinnerItem filled in so far...
                    request.meta['item'] = NWinnerItem(**wdata) 
                    request.meta['debug_call_location'] = 'list to bio' #DEBUG
                    # if parse got all the info just from this page, we would
                    # put the info in an NWinnerItem and 'yield item' so that
                    # this is an item generator.  However, we need to follow 
                    # the links to the bio pages, so instead, we make parse
                    # a generator of consumable requests to bio pages and
                    # pass along the NWinnerItem in the request.meta
                    yield request 

    def process_winner_li(self, w, country=None):
        ''' Process a winner's <li> tag, adding country of birth or
        nationality, as applicable'''
        BASE_URL = 'https://en.wikipedia.org'

        wdata = {}
        wdata['link'] = BASE_URL + w.xpath('a/@href').extract()[0]

        text = ' '.join(w.xpath('descendant-or-self::text()').extract())
        #get comma-delimited name and strip trailing whitespace
        wdata['name'] = text.split(',')[0].strip()

        year = re.findall('\d{4}', text)
        if year:
            wdata['year'] = int(year[0])
        else:
            wdata['year'] = 0
            print('Oops, no year in ', text)

        category = re.findall('Physics|Chemistry|Physiology or Medicine|'\
                'Literature|Peace|Economics', text)
        if category:
            wdata['category'] = category[0]
        else:
            wdata['category'] = ''
            print('Oops, no category in ', text)

        if country:
            if text.find('*') != -1: #asterisk following name indicates country is birth
                wdata['country'] = ''
                wdata['born_in'] = country
            else:
                wdata['country'] = country
                wdata['born_in'] = ''

        # store a copy of the link's text string
        # for manual corrections
        wdata['text'] = text
        return wdata

    def error_handler(self, failure):
        # log all failures
        self.logger.error(repr(failure))

        # in case you want to do something special for some errors,
        # you may need the failure's type:
        if failure.check(HttpError):
            # these exceptions come from HttpError spider middleware
            # you can get the non-200 response
            response = failure.value.response
            self.logger.error('HttpError on %s', response.url)
        elif failure.check(DNSLookupError):
            # this is the original request
            request = failure.request
            self.logger.error('DNSLookupError on %s', request.url)
        elif failure.check(TimeoutError, TCPTimedOutError):
            request = failure.request
            self.logger.error('TimeoutError on %s', request.url)

    def parse_bio(self, response):
        '''The callback method for parsing bio page requests generated by parse'''
        item = response.meta['item'] # the NWinnerItem filled in up to this point

        #from scrapy.shell import inspect_response #DEBUG
        #inspect_response(response, self) #DEBUG

        # get the URL of the place on wikibase where the bio info is kept.  It tends
        # to have a more consistent HTML structure at wikibase.
        href = response.xpath('//li[@id="t-wikibase"]/a/@href').extract()
        if href:
            request = scrapy.Request(href[0],
                                    callback=self.parse_wikidata,
                                    dont_filter=True)
            request.meta['item'] = item
            request.meta['debug_call_location'] = 'bio to wikidata' #DEBUG
            yield request

    def parse_wikidata(self, response):
        item = response.meta['item']
        # these property_codes were gleaned from the programmatically generated
        # wikidata page.  We need these codes to navigate to the right place
        property_codes = [
            {'name':'date_of_birth', 'code':'P569'},
            {'name':'date_of_death', 'code':'P576'},
            {'name':'place_of_birth', 'code':'P19', 'link':True},
            {'name':'place_of_death', 'code':'P20', 'link':True},
            {'name':'gender', 'code':'P21', 'link':True}
        ]
        
        p_template = '//*[@id="{code}"]/div[2]/div/div/div[2]' \
                    '/div[1]/div/div[2]/div[2]/{link_html}/text()'

        for prop in property_codes:
            link_html = ''
            if prop.get('link'):
                link_html = '/a'
            sel = response.xpath(p_template.format(code=prop['code'],
                                                    link_html=link_html))
            if sel:
                item[prop['name']] = sel[0].extract()
        yield item

