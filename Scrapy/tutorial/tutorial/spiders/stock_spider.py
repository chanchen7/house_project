import scrapy
import re
import datetime
from tutorial.stock_info import StockInfo

class DmozSpider(scrapy.Spider):
    name = "stock"
    allowed_domains = ["com"]
    start_urls = [
        "http://quote.eastmoney.com/stocklist.html"
        #"http://www.aigaogao.com/tools/history.html?s=601985"
    ]
    


    def parse(self, response):
        homesearch = response.xpath('//div[@id="quotesearch"]')
        for sel in homesearch.xpath('ul/li'):
            title = "%s" % (sel.xpath('a/text()').extract())
            pattern = re.compile(r'.+\((6|0)[0-9]{5}\)')
            matchObj = pattern.search(title)
            if matchObj:
                stock_title = matchObj.group().split('\'')[1].split('(')[0]
                stock_code = matchObj.group().split('(')[1].split(')')[0]
                url = "http://www.aigaogao.com/tools/history.html?s=" + stock_code
                yield scrapy.Request(url, meta={'stock_code': stock_code, 'stock_name': stock_title}, callback=self.parse_detail)
            else:
                continue
    
    def parse_detail(self, response):
        items = []
        quotesearch = response.xpath('//div[@id="ctl16_contentdiv"]//table[@class="data"]')
        for sel in quotesearch.xpath('tr'):
            if not sel.xpath('td/a/text()').extract():
                continue
            tds = sel.xpath('td')
            item = StockInfo()
            item['stock_code'] = response.meta['stock_code']
            item['stock_name'] = response.meta['stock_name']
            
            dateStr = sel.xpath('td/a/text()').extract_first()
            item['date'] = datetime.datetime.strptime(dateStr, '%m/%d/%Y').strftime('%Y-%m-%d')

            item['start_value'] = tds[1].xpath('text()').extract_first()
            item['end_value'] = tds[4].xpath('text()').extract_first()
            item['max_value'] = tds[2].xpath('text()').extract_first()
            item['min_value'] = tds[3].xpath('text()').extract_first()
            item['volume'] = tds[5].xpath('text()').extract_first().replace(',','')
            item['turn_volume'] = tds[6].xpath('text()').extract_first().replace(',','')
            items.append(item)
        return items

                
        
