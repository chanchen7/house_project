import scrapy
import time
from lianjia.items import HouseItem
from lianjia.items import CommunityItem
from lianjia.items import HousePriceItem
from lianjia.mongo.mongo_tools import MongoDBProxy

class HouseSpider(scrapy.Spider):
    name = "house"
    allowed_domains = ["com"]
    start_urls = [
        "https://nj.lianjia.com/ershoufang/gulou/ep200/",
        "https://nj.lianjia.com/ershoufang/gulou/bp200ep300/",
        "https://nj.lianjia.com/ershoufang/gulou/bp300ep500/",
        "https://nj.lianjia.com/ershoufang/gulou/bp500ep100000/",

        "https://nj.lianjia.com/ershoufang/jianye/ep200/",
        "https://nj.lianjia.com/ershoufang/jianye/bp200ep300/",
        "https://nj.lianjia.com/ershoufang/jianye/bp300ep500/",
        "https://nj.lianjia.com/ershoufang/jianye/bp500ep100000/",

        "https://nj.lianjia.com/ershoufang/qinhuai/ep200/",
        "https://nj.lianjia.com/ershoufang/qinhuai/bp200ep300/",
        "https://nj.lianjia.com/ershoufang/qinhuai/bp300ep500/",
        "https://nj.lianjia.com/ershoufang/qinhuai/bp500ep100000/",

        "https://nj.lianjia.com/ershoufang/xuanwu/ep200/",
        "https://nj.lianjia.com/ershoufang/xuanwu/bp200ep300/",
        "https://nj.lianjia.com/ershoufang/xuanwu/bp300ep500/",
        "https://nj.lianjia.com/ershoufang/xuanwu/bp500ep100000/",

        "https://nj.lianjia.com/ershoufang/yuhuatai/ep200/",
        "https://nj.lianjia.com/ershoufang/yuhuatai/bp200ep300/",
        "https://nj.lianjia.com/ershoufang/yuhuatai/bp300ep500/",
        "https://nj.lianjia.com/ershoufang/yuhuatai/bp500ep100000/",

        "https://nj.lianjia.com/ershoufang/qixia/ep200/",
        "https://nj.lianjia.com/ershoufang/qixia/bp200ep300/",
        "https://nj.lianjia.com/ershoufang/qixia/bp300ep500/",
        "https://nj.lianjia.com/ershoufang/qixia/bp500ep100000/",

        "https://nj.lianjia.com/ershoufang/jiangning/ep200/",
        "https://nj.lianjia.com/ershoufang/jiangning/bp200ep300/",
        "https://nj.lianjia.com/ershoufang/jiangning/bp300ep500/",
        "https://nj.lianjia.com/ershoufang/jiangning/bp500ep100000/",

        "https://nj.lianjia.com/ershoufang/pukou/ep200/",
        "https://nj.lianjia.com/ershoufang/pukou/bp200ep300/",
        "https://nj.lianjia.com/ershoufang/pukou/bp300ep500/",
        "https://nj.lianjia.com/ershoufang/pukou/bp500ep100000/",

        "https://nj.lianjia.com/ershoufang/liuhe/",
        "https://nj.lianjia.com/ershoufang/lishui/",
        "https://nj.lianjia.com/ershoufang/gaochun/"
    ]

    def parse(self, response):
        self.proxy = MongoDBProxy()
        homesearch = response.xpath('//div[@class="content "]//div[@class="leftContent"]')   
        items = []
        for sel in homesearch.xpath('ul/li'):
            item = HousePriceItem()
            lianjia_id = sel.xpath('a[@class="noresultRecommend img "]/@data-housecode').extract_first()
            community_url = sel.xpath('div[@class="info clear"]/div[@class="address"]/div[@class="houseInfo"]/a/@href').extract_first()
            community_id = community_url.split('xiaoqu/')[1].split('/')[0]
            
            item['house_id'] = lianjia_id       #链家编号
            item['capture_time'] = time.strftime("%Y%m%d%H%M%S", time.localtime())   #截获时间
            item['unit_price'] = sel.xpath('div[@class="info clear"]/div[@class="priceInfo"]/div[@class="unitPrice"]/@data-price').extract_first()     #每平米单价
            item['total_price'] = sel.xpath('div[@class="info clear"]/div[@class="priceInfo"]/div[@class="totalPrice"]/span/text()').extract_first()    #总价
                
            followInfo = sel.xpath('div[@class="info clear"]/div[@class="followInfo"]/text()').extract_first()
            item['follow_total'] = followInfo.split('人关注')[0]   #总关注 
            item['view_total'] = followInfo.split('/ 共')[1].split('次带看')[0]    #总带看
            item['community'] = sel.xpath('div[@class="info clear"]/div[@class="address"]/div[@class="houseInfo"]/a/text()').extract_first().rstrip()
            item['community_id'] = community_id
            items.append(item)
            if self.proxy.get_community_item(community_id) == None:
                yield scrapy.Request(community_url, callback=self.parse_detail_community)
            else:
                pass

            if self.proxy.get_house_item(lianjia_id) == None:
                detail_url = sel.xpath('a/@href').extract_first()
                if not detail_url is None:
                    yield scrapy.Request(detail_url, callback=self.parse_detail)   #详细信息
        yield self.proxy.insert_house_price_item(items)
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
        if len(infotables) > 6:
            item['build_year'] = infotables[0].xpath('span[last()]/text()').extract_first().split('年')[0]     #建造时间
            item['total_households'] = infotables[6].xpath('span[last()]/text()').extract_first().split('户')[0]    #总户数
            item['house_property'] = infotables[3].xpath('span[last()]/text()').extract_first()      #物业
            item['developer'] = infotables[4].xpath('span[last()]/text()').extract_first()      #开发商
            item['property_fee'] = infotables[2].xpath('span[last()]/text()').extract_first()   #物业费
        self.proxy.insert_community_item(item)
        #return item

    def parse_detail(self, response):
        item = HouseItem()
        item['name'] = response.xpath('//div[@class="sellDetailHeader"]//h1[@class="main"]/text()').extract_first()

        overview = response.xpath('//div[@class="overview"]//div[@class="content"]')
        item['house_id'] = overview.xpath('div[@class="aroundInfo"]/div[@class="houseRecord"]/span[@class="info"]/text()').extract_first()
        
        item['region'] = overview.xpath('div[@class="aroundInfo"]/div[@class="areaName"]/span[@class="info"]/a')[0].xpath('text()').extract_first()

        item['community_name'] = overview.xpath('div[@class="aroundInfo"]//a[@class="info "]/text()').extract_first()
        item['community_id'] = overview.xpath('div[@class="aroundInfo"]//a[@class="info "]/@href').extract_first().split('/')[2]
        

        baseinfo = response.xpath('//div[@class="newwrap baseinform"]/div/div[@class="introContent"]/div[@class="base"]')
        basetables = baseinfo.xpath('div[@class="content"]/ul/li')

        item['style'] = basetables[0].xpath('text()').extract_first()
        item['floor'] = basetables[1].xpath('text()').extract_first()
        item['built_up_area'] = basetables[2].xpath('text()').extract_first()
        if len(basetables) > 4 :
            item['inner_area'] = basetables[4].xpath('text()').extract_first()
            item['orientation'] = basetables[6].xpath('text()').extract_first()
            item['decoration'] = basetables[8].xpath('text()').extract_first()
        else:
            item['inner_area'] = "未知"
            item['orientation'] = "未知"
            item['decoration'] = "未知"
        if len(basetables) > 10 :
            item['elevator'] = basetables[10].xpath('text()').extract_first()
        else:
            item['elevator'] = "未知"
        if len(basetables) > 11 :
            item['property_right_age_limit'] = basetables[11].xpath('text()').extract_first()
        else:
            item['property_right_age_limit'] = "未知"

        transactioninfo = response.xpath('//div[@class="newwrap baseinform"]/div/div[@class="introContent"]/div[@class="transaction"]')
        transactiontables = transactioninfo.xpath('div[@class="content"]/ul/li')
        if len(transactiontables) > 4 :
            item['list_time'] = transactiontables[0].xpath('span[last()]/text()').extract_first()
            item['last_sign_time'] = transactiontables[2].xpath('span[last()]/text()').extract_first()
            item['transaction_type'] = transactiontables[1].xpath('span[last()]/text()').extract_first()
            item['house_type'] = transactiontables[3].xpath('span[last()]/text()').extract_first()
            item['tax'] = transactiontables[4].xpath('span[last()]/text()').extract_first()

        item['href'] = response.url
        self.proxy.insert_house_item(item)   
        #return item