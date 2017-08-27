import scrapy
import re

BASE_URL = 'https://en.wikipedia.org'

class NWinnerItemBio(scrapy.Item):
    link = scrapy.Field()
    name = scrapy.Field()
    mini_bio = scrapy.Field()
    image_urls = scrapy.Field()
    bio_image = scrapy.Field()
    images = scrapy.Field()


class NWinnerSpiderBio(scrapy.Spider):
    '''Scrapes the country and link text of Nobel winners'''
    name = 'minibio_nwinners'
    allowed_domains = ['en-wikipedia.org']
    start_urls = [
        'https://en.wikipedia.org/wiki/List_of_Nobel_laureates_by_country' ]

    # we could just specify the pipelines in setting.py, but that sets
    # the pipelines for all the spiders in the project.  Rather than do
    # that, set the pipeline here for just this spider
    custom_settings = {
        'ITEM_PIPELINES': {'nobel_winners.pipelines.NobelImagePipeline':1} }

    # a parse method to deal with the HTTP response
    def parse(self, response):
        filename = response.url.split('/')[-1]
        h2s = response.xpath('//h2')
        for h2 in h2s:
            country = h2.xpath('span[@class="mw-headline"]/text()').extract()
            if country:
                winners = h2.xpath('following-sibling::ol[1]')
                for w in winners.xpath('li'):
                    wdata = {}
                    wdata['link'] = BASE_URL + w.xpath('a/@href').extract()[0]
                    #process the winner's bio page with get_mini_bio method
                    request = scrapy.Request(wdata['link'], 
                                        callback=self.get_mini_bio,
                                        dont_filter=True
                                        )
                    #give response access to NWinnerItem filled in so far...
                    request.meta['item'] = NWinnerItemBio(**wdata) 
                    request.meta['debug_call_location'] = 'list to bio' #DEBUG
                    yield request 

    def get_mini_bio(self, response):
        '''Get the winner's bio-text and photo'''
        BASE_URL_ESCAPED = 'https:\/\/en.wikipedia.org'
        item = response.meta['item']
        item['image_urls'] = []
        # this next xpath targets the first (and only) image in the table of
        # class infobox and gets its source (src) attribute
        img_src = response.xpath('//table[contains(@class, "infobox")]//img/@src')
        if img_src:
            item['image_urls'] = ['https:' + img_src[0].extract()]

        mini_bio = ''
        # the bio is the first several paragraphs (<p>) after the div of id
        # "mw:content-text".  It stops at the first blank paragraph (<p></p>).
        # this next xpath gets all the paragraphs that are children of the 
        # (div) with id "mw:content-text" and if their text is empty 
        # (text() == False) then it calls normalize-space(.) command to force
        # the contents of the paragraph to an empty string. (the "." represents
        # the p-node in question.  This is to make sure any empty paragraph
        # matches the stop-point marking theh end of the intro section of the
        # biography
        paras = response.xpath('//*[@id="mw-content-text"]'\
                                '/p[text() or normalize-space(.)=""]').extract()
        for p in paras:
            if p == '<p></p>': # the bios stop point...
                break
            mini_bio += p

        # convert links in the mini_bio into full absolute links instead of 
        # relative links
        mini_bio = mini_bio.replace('href="/wiki', 'href="' + BASE_URL + '/wiki')
        mini_bio = mini_bio.replace('href="#', item['link'] + '#')
        item['mini_bio'] = mini_bio
        yield item
