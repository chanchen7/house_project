import scrapy
import time
from lianjia.items import TransactionItem
from lianjia.items import HouseItem
from lianjia.items import CommunityItem
from lianjia.mongo.mongo_tools import MongoDBProxy

class HouseSpider(scrapy.Spider):
    name = "house_transaction"
    allowed_domains = ["com"]
    start_urls = [
        "https://nj.lianjia.com/chengjiao/gulou/ep200/",
        "https://nj.lianjia.com/chengjiao/gulou/bp200ep300/",
        "https://nj.lianjia.com/chengjiao/gulou/bp300ep500/",
        "https://nj.lianjia.com/chengjiao/gulou/bp500ep100000/",

        "https://nj.lianjia.com/chengjiao/jianye/ep200/",
        "https://nj.lianjia.com/chengjiao/jianye/bp200ep300/",
        "https://nj.lianjia.com/chengjiao/jianye/bp300ep500/",
        "https://nj.lianjia.com/chengjiao/jianye/bp500ep100000/",

        "https://nj.lianjia.com/chengjiao/qinhuai/ep200/",
        "https://nj.lianjia.com/chengjiao/qinhuai/bp200ep300/",
        "https://nj.lianjia.com/chengjiao/qinhuai/bp300ep500/",
        "https://nj.lianjia.com/chengjiao/qinhuai/bp500ep100000/",

        "https://nj.lianjia.com/chengjiao/xuanwu/ep200/",
        "https://nj.lianjia.com/chengjiao/xuanwu/bp200ep300/",
        "https://nj.lianjia.com/chengjiao/xuanwu/bp300ep500/",
        "https://nj.lianjia.com/chengjiao/xuanwu/bp500ep100000/",

        "https://nj.lianjia.com/chengjiao/yuhuatai/ep200/",
        "https://nj.lianjia.com/chengjiao/yuhuatai/bp200ep300/",
        "https://nj.lianjia.com/chengjiao/yuhuatai/bp300ep500/",
        "https://nj.lianjia.com/chengjiao/yuhuatai/bp500ep100000/",

        "https://nj.lianjia.com/chengjiao/qixia/ep200/",
        "https://nj.lianjia.com/chengjiao/qixia/bp200ep300/",
        "https://nj.lianjia.com/chengjiao/qixia/bp300ep500/",
        "https://nj.lianjia.com/chengjiao/qixia/bp500ep100000/",

        "https://nj.lianjia.com/chengjiao/jiangning/ep200/",
        "https://nj.lianjia.com/chengjiao/jiangning/bp200ep300/",
        "https://nj.lianjia.com/chengjiao/jiangning/bp300ep500/",
        "https://nj.lianjia.com/chengjiao/jiangning/bp500ep100000/",

        "https://nj.lianjia.com/chengjiao/pukou/ep200/",
        "https://nj.lianjia.com/chengjiao/pukou/bp200ep300/",
        "https://nj.lianjia.com/chengjiao/pukou/bp300ep500/",
        "https://nj.lianjia.com/chengjiao/pukou/bp500ep100000/",

        "https://nj.lianjia.com/chengjiao/liuhe/",
        "https://nj.lianjia.com/chengjiao/lishui/",
        "https://nj.lianjia.com/chengjiao/gaochun/"
    ]

    def parse(self, response):
        self.proxy = MongoDBProxy()
        homesearch = response.xpath('//div[@class="content"]//div[@class="leftContent"]')
        for sel in homesearch.xpath('ul/li'):
            lianjia_id = sel.xpath('a/@href').extract_first().split('chengjiao/')[1].split('.html')[0]
            if self.proxy.get_house_item(lianjia_id) == None:
                detail_url = sel.xpath('a/@href').extract_first()
                yield scrapy.Request(detail_url, callback=self.parse_detail)   #详细信息
            transactionDate = sel.xpath('//div[@class="address"]/div[@class="dealDate"]/text()').extract_first()
            if transactionDate == "近30天内成交" :
                transactionDate = time.strftime("%Y%m%d", time.localtime())
            else :
                transactionDate = transactionDate.replace(".", "")
            if not transactionDate is None :
                if self.proxy.is_house_transaction_item_exist(lianjia_id, transactionDate) == False:
                    detail_url = sel.xpath('a/@href').extract_first()
                    yield scrapy.Request(detail_url, callback=self.parse_detail_transaction)   
        # 下一页
        page_data = homesearch.xpath('div[@class="contentBottom clear"]/div[@class="page-box fr"]/div/@page-data').extract_first()
        if not page_data is None:
            splitStr = homesearch.xpath('div[@class="contentBottom clear"]/div[@class="page-box fr"]/div/@page-data').extract_first().split(':')
            pageUrl = homesearch.xpath('div[@class="contentBottom clear"]/div[@class="page-box fr"]/div/@page-url').extract_first()
            total_page = int(splitStr[1].split(',')[0])
            cur_page = int(splitStr[2].split('}')[0])
            if cur_page < total_page:
                cur_page += 1
                url = "https://nj.lianjia.com" + pageUrl.replace("{page}", str(cur_page))
                yield scrapy.Request(url, callback=self.parse)
        
    def parse_detail_community(self, response):
        item = CommunityItem()
        item['community_id'] = response.url.split('xiaoqu/')[1].split('/')[0]   #小区id
        item['community'] = response.xpath('//h1[@class="detailTitle"]/text()').extract_first()
        
        infotables = response.xpath('//div[@class="xiaoquInfo"]/div[@class="xiaoquInfoItem"]')
        item['build_year'] = infotables[0].xpath('span[last()]/text()').extract_first().split('年')[0]     #建造时间
        item['total_households'] = infotables[6].xpath('span[last()]/text()').extract_first().split('户')[0]    #总户数
        item['house_property'] = infotables[3].xpath('span[last()]/text()').extract_first()      #物业
        item['developer'] = infotables[4].xpath('span[last()]/text()').extract_first()      #开发商
        item['property_fee'] = infotables[2].xpath('span[last()]/text()').extract_first()   #物业费
        self.proxy.insert_community_item(item)
        #return item

    def parse_detail_transaction(self, response):
        transactionItem = TransactionItem()
        transactionItem["house_id"] = response.xpath('//@data-lj_action_resblock_id').extract_first()       #链家编号
        transactionItem["transaction_price"] = response.xpath('//div[@class="price"]/span/i/text()').extract_first()  #成交总价
        transactionItem["transaction_unit_price"] = response.xpath('//div[@class="price"]/b/text()').extract_first()     #成交单价

        transactionItem['community_id'] = response.xpath('//@data-lj_action_housedel_id').extract_first()
        transactionItem['community'] = response.xpath('//h1[@class="index_h1"]/text()').extract_first().split(' ')[0]
        
        
        transactionMsgs = response.xpath('//div[@class="info fr"]/div[@class="msg"]/span')
        transactionItem["list_price"] = transactionMsgs[0].xpath('label/text()').extract_first()     #挂牌价
        transactionItem["follow_total"] = transactionMsgs[4].xpath('label/text()').extract_first()   #总关注
        transactionItem["view_total"] = transactionMsgs[3].xpath('label/text()').extract_first()     #总带看
        transactionItem["transaction_period"] = transactionMsgs[1].xpath('label/text()').extract_first()     #成交周期
        transactionItem["transaction_date"] = response.xpath('//div[@class="wrapper"]/span/text()').extract_first().split(' ')[0].replace(".", "-")       #成交日期
        self.proxy.insert_house_transaction_item(transactionItem)

    def parse_detail(self, response):
        item = HouseItem()
        item['name'] = response.xpath('//h1[@class="index_h1"]/text()').extract_first()
        item['house_id'] = response.xpath('//@data-lj_action_resblock_id').extract_first()
        item['community_id'] = response.xpath('//@data-lj_action_housedel_id').extract_first()
        item['community_name'] = item['name'].split(' ')[0]

        if self.proxy.get_community_item(item['community_id']) == None :
            yield scrapy.Request("https://nj.lianjia.com/xiaoqu/" + item['community_id'] + "/", callback=self.parse_detail_community)
        
        tmpHrefs = response.xpath('//div[@class="deal-bread"]/a')
        if len(tmpHrefs) > 2 :
            item['region'] = tmpHrefs[2].xpath('text()').extract_first().split('二手房')[0]
            
        baseinfo = response.xpath('//div[@class="newwrap baseinform"]/div[@class="introContent"]/div[@class="base"]')
        basetables = baseinfo.xpath('div[@class="content"]/ul/li')

        item['style'] = basetables[0].xpath('text()').extract_first().rstrip()
        item['floor'] = basetables[1].xpath('text()').extract_first().rstrip()
        item['built_up_area'] = basetables[2].xpath('text()').extract_first().rstrip()
        item['inner_area'] = basetables[4].xpath('text()').extract_first().rstrip()
        item['orientation'] = basetables[6].xpath('text()').extract_first().rstrip()
        item['decoration'] = basetables[8].xpath('text()').extract_first().rstrip()
        if len(basetables) > 10 :
            item['elevator'] = basetables[10].xpath('text()').extract_first().rstrip()
        else:
            item['elevator'] = "未知"
        if len(basetables) > 12 :
            item['property_right_age_limit'] = basetables[12].xpath('text()').extract_first().rstrip()
        else:
            item['property_right_age_limit'] = "未知"

        transactioninfo = response.xpath('//div[@class="newwrap baseinform"]/div[@class="introContent"]/div[@class="transaction"]')
        transactiontables = transactioninfo.xpath('div[@class="content"]/ul/li')

        item['list_time'] = transactiontables[2].xpath('text()').extract_first().rstrip()
        item['transaction_type'] = transactiontables[1].xpath('text()').extract_first().rstrip()
        item['house_type'] = transactiontables[3].xpath('text()').extract_first().rstrip()
        item['tax'] = transactiontables[4].xpath('text()').extract_first().rstrip()

        item['last_sign_time'] = response.xpath('//div[@class="wrapper"]/span/text()').extract_first().split(' ')[0].replace(".", "-")

        item['href'] = response.url
        self.proxy.insert_house_item(item)   
        #return item