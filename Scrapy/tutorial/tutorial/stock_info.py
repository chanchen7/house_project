import scrapy


class StockInfo(scrapy.Item):
    stock_code = scrapy.Field()
    stock_name = scrapy.Field()
    date = scrapy.Field()
    start_value = scrapy.Field()
    end_value = scrapy.Field()
    max_value = scrapy.Field()
    min_value = scrapy.Field()
    volume = scrapy.Field()
    turn_volume = scrapy.Field()