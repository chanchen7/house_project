import scrapy
import re
from tutorial.items import StockItem

class DmozSpider(scrapy.Spider):
    name = "eastmoney"
    allowed_domains = ["eastmoney.com"]
    start_urls = [
        "http://quote.eastmoney.com/stocklist.html"

    ]

    def parse(self, response):
        quotesearch = response.xpath('//div[@id="quotesearch"]')
        for sel in quotesearch.xpath('ul/li'):
            title = "%s" % (sel.xpath('a/text()').extract())
            pattern = re.compile(r'.+\((6|0)[0-9]{5}\)')
            matchObj = pattern.search(title)
            if matchObj:
                item = StockItem()
                item['code'] = matchObj.group().split('(')[1].split(')')[0]
                item['name'] = matchObj.group().split('\'')[1].split('(')[0]
                yield item
            else:
                continue
        #filename = response.url.split("/")[-2]
        #with open(filename, 'wb') as f:
            #f.write(response.body)
