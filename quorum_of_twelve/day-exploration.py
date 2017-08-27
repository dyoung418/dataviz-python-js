# coding: utf-8
response.status
h2s = response.xpath('//h2')
h2s[0].extract()
h2s[1].extract()
h2s[2].extract()
len(h2s)
tables = h2s[2].xpath('following-sibling::table[@class="wikitable"]')
len(tables)
tables[0].extract()
tables.xpath('ol')
tables.xpath('ul')
tables.xpath('td')
#tables.xpath('tr')
