# coding: utf-8
h2s = response.xpath('//h2')
len(h2s)
h2 = h2s[0]
h2.extract()
h2s[1].extract()
h2s[2].extract() # this 3rd element has the first country (Argentina)
h2_args = h2s[2]
# doing this next xpath off h2_args makes the xpath relative to h2_args
country = h2_args.xpath('span[@class="mw-headline"]/text()').extract() #returns a list (of len=1 in this case)

ol_arg = h2_args.xpath('following-sibling::ol[1]') #first ol sibling after h2_args
lis_arg = ol_arg.xpath('li')
len(lis_arg)
lis_arg[0].extract() #look at this first
li = lis_arg[0]
name = li.xpath('a//text()')[0].extract()
name
list_text = li.xpath('descendant-or-self::text()').extract() # get all text, striping various HTML tags <a>, <span> etc.
list_text
' '.join(list_text)
