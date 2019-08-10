#coding:utf-8
import scrapy
import time
import sys
#sys.path.append('/usr/local/lianjia/mongo')
sys.path.append('K:\Backup\代码\GitRepository\house_project\Scrapy\lianjia\lianjia\mongo')
from lianjia.items import HouseItem
from lianjia.items import CommunityItem
from lianjia.items import HousePriceItem
from mongo_tools import MongoDBProxy

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

        "https://nj.lianjia.com/ershoufang/jiangning/ep120/",
        "https://nj.lianjia.com/ershoufang/jiangning/bp120ep170/",
        "https://nj.lianjia.com/ershoufang/jiangning/bp170ep200/",
        "https://nj.lianjia.com/ershoufang/jiangning/bp200ep230/",
        "https://nj.lianjia.com/ershoufang/jiangning/bp230ep260/",
        "https://nj.lianjia.com/ershoufang/jiangning/bp260ep300/",
        "https://nj.lianjia.com/ershoufang/jiangning/bp300ep370/",
        "https://nj.lianjia.com/ershoufang/jiangning/bp370ep500/",
        "https://nj.lianjia.com/ershoufang/jiangning/bp500ep100000/",

        "https://nj.lianjia.com/ershoufang/pukou/ep170/",
        "https://nj.lianjia.com/ershoufang/pukou/bp170ep200/",
        "https://nj.lianjia.com/ershoufang/pukou/bp200ep230/",
        "https://nj.lianjia.com/ershoufang/pukou/bp230ep260/",
        "https://nj.lianjia.com/ershoufang/pukou/bp260ep300/",
        "https://nj.lianjia.com/ershoufang/pukou/bp300ep370/",
        "https://nj.lianjia.com/ershoufang/pukou/bp370ep500/",
        "https://nj.lianjia.com/ershoufang/pukou/bp500ep100000/",

        "https://nj.lianjia.com/ershoufang/liuhe/ep200/",
        "https://nj.lianjia.com/ershoufang/liuhe/bp200ep300/",
        "https://nj.lianjia.com/ershoufang/liuhe/bp300ep500/",
        "https://nj.lianjia.com/ershoufang/liuhe/bp500ep100000/",

        "https://nj.lianjia.com/ershoufang/lishui/ep200/",
        "https://nj.lianjia.com/ershoufang/lishui/bp200ep300/",
        "https://nj.lianjia.com/ershoufang/lishui/bp300ep500/",
        "https://nj.lianjia.com/ershoufang/lishui/bp500ep100000/",

        "https://nj.lianjia.com/ershoufang/gaochun/",

	    "https://sh.lianjia.com/ershoufang/pudong/ep200/",
        "https://sh.lianjia.com/ershoufang/pudong/bp200ep300/",
        "https://sh.lianjia.com/ershoufang/pudong/bp300ep400/",
        "https://sh.lianjia.com/ershoufang/pudong/bp400ep500/",
        "https://sh.lianjia.com/ershoufang/pudong/bp500ep800/",
        "https://sh.lianjia.com/ershoufang/pudong/bp800ep100000/",

        "https://sh.lianjia.com/ershoufang/minhang/ep200/",
        "https://sh.lianjia.com/ershoufang/minhang/bp200ep300/",
        "https://sh.lianjia.com/ershoufang/minhang/bp300ep500/",
        "https://sh.lianjia.com/ershoufang/minhang/bp500ep100000/",

        "https://sh.lianjia.com/ershoufang/baoshan/ep200/",
        "https://sh.lianjia.com/ershoufang/baoshan/bp200ep300/",
        "https://sh.lianjia.com/ershoufang/baoshan/bp300ep500/",
        "https://sh.lianjia.com/ershoufang/baoshan/bp500ep100000/",

        "https://sh.lianjia.com/ershoufang/xuhui/ep200/",
        "https://sh.lianjia.com/ershoufang/xuhui/bp200ep300/",
        "https://sh.lianjia.com/ershoufang/xuhui/bp300ep500/",
        "https://sh.lianjia.com/ershoufang/xuhui/bp500ep100000/",

        "https://sh.lianjia.com/ershoufang/putuo/ep200/",
        "https://sh.lianjia.com/ershoufang/putuo/bp200ep300/",
        "https://sh.lianjia.com/ershoufang/putuo/bp300ep500/",
        "https://sh.lianjia.com/ershoufang/putuo/bp500ep100000/",

        "https://sh.lianjia.com/ershoufang/yangpu/ep200/",
        "https://sh.lianjia.com/ershoufang/yangpu/bp200ep300/",
        "https://sh.lianjia.com/ershoufang/yangpu/bp300ep500/",
        "https://sh.lianjia.com/ershoufang/yangpu/bp500ep100000/",

        "https://sh.lianjia.com/ershoufang/changning/ep200/",
        "https://sh.lianjia.com/ershoufang/changning/bp200ep300/",
        "https://sh.lianjia.com/ershoufang/changning/bp300ep500/",
        "https://sh.lianjia.com/ershoufang/changning/bp500ep100000/",

        "https://sh.lianjia.com/ershoufang/songjiang/ep200/",
        "https://sh.lianjia.com/ershoufang/songjiang/bp200ep300/",
        "https://sh.lianjia.com/ershoufang/songjiang/bp300ep500/",
        "https://sh.lianjia.com/ershoufang/songjiang/bp500ep100000/",

        "https://sh.lianjia.com/ershoufang/jiading/ep200/",
        "https://sh.lianjia.com/ershoufang/jiading/bp200ep300/",
        "https://sh.lianjia.com/ershoufang/jiading/bp300ep500/",
        "https://sh.lianjia.com/ershoufang/jiading/bp500ep100000/",

        "https://sh.lianjia.com/ershoufang/huangpu/ep200/",
        "https://sh.lianjia.com/ershoufang/huangpu/bp200ep300/",
        "https://sh.lianjia.com/ershoufang/huangpu/bp300ep500/",
        "https://sh.lianjia.com/ershoufang/huangpu/bp500ep100000/",

        "https://sh.lianjia.com/ershoufang/jingan/ep200/",
        "https://sh.lianjia.com/ershoufang/jingan/bp200ep300/",
        "https://sh.lianjia.com/ershoufang/jingan/bp300ep500/",
        "https://sh.lianjia.com/ershoufang/jingan/bp500ep100000/",

        "https://sh.lianjia.com/ershoufang/zhabei/ep200/",
        "https://sh.lianjia.com/ershoufang/zhabei/bp200ep300/",
        "https://sh.lianjia.com/ershoufang/zhabei/bp300ep500/",
        "https://sh.lianjia.com/ershoufang/zhabei/bp500ep100000/",

        "https://sh.lianjia.com/ershoufang/hongkou/ep200/",
        "https://sh.lianjia.com/ershoufang/hongkou/bp200ep300/",
        "https://sh.lianjia.com/ershoufang/hongkou/bp300ep500/",
        "https://sh.lianjia.com/ershoufang/hongkou/bp500ep100000/",

        "https://sh.lianjia.com/ershoufang/qingpu/ep200/",
        "https://sh.lianjia.com/ershoufang/qingpu/bp200ep300/",
        "https://sh.lianjia.com/ershoufang/qingpu/bp300ep500/",
        "https://sh.lianjia.com/ershoufang/qingpu/bp500ep100000/",

        "https://sh.lianjia.com/ershoufang/fengxian/",
        "https://sh.lianjia.com/ershoufang/jinshan/",
        "https://sh.lianjia.com/ershoufang/chongming/",
        "https://sh.lianjia.com/ershoufang/shanghaizhoubian",

        "https://hz.lianjia.com/ershoufang/xihu/ep200/",
        "https://hz.lianjia.com/ershoufang/xihu/bp200ep300/",
        "https://hz.lianjia.com/ershoufang/xihu/bp300ep500/",
        "https://hz.lianjia.com/ershoufang/xihu/bp500ep100000/",

        "https://hz.lianjia.com/ershoufang/xiacheng/ep200/",
        "https://hz.lianjia.com/ershoufang/xiacheng/bp200ep300/",
        "https://hz.lianjia.com/ershoufang/xiacheng/bp300ep500/",
        "https://hz.lianjia.com/ershoufang/xiacheng/bp500ep100000/",

        "https://hz.lianjia.com/ershoufang/jianggan/ep200/",
        "https://hz.lianjia.com/ershoufang/jianggan/bp200ep300/",
        "https://hz.lianjia.com/ershoufang/jianggan/bp300ep500/",
        "https://hz.lianjia.com/ershoufang/jianggan/bp500ep100000/",

        "https://hz.lianjia.com/ershoufang/gongshu/ep200/",
        "https://hz.lianjia.com/ershoufang/gongshu/bp200ep300/",
        "https://hz.lianjia.com/ershoufang/gongshu/bp300ep500/",
        "https://hz.lianjia.com/ershoufang/gongshu/bp500ep100000/",

        "https://hz.lianjia.com/ershoufang/shangcheng/ep200/",
        "https://hz.lianjia.com/ershoufang/shangcheng/bp200ep300/",
        "https://hz.lianjia.com/ershoufang/shangcheng/bp300ep500/",
        "https://hz.lianjia.com/ershoufang/shangcheng/bp500ep100000/",

        "https://hz.lianjia.com/ershoufang/binjiang/ep200/",
        "https://hz.lianjia.com/ershoufang/binjiang/bp200ep300/",
        "https://hz.lianjia.com/ershoufang/binjiang/bp300ep500/",
        "https://hz.lianjia.com/ershoufang/binjiang/bp500ep100000/",

        "https://hz.lianjia.com/ershoufang/yuhang/ep200/",
        "https://hz.lianjia.com/ershoufang/yuhang/bp200ep300/",
        "https://hz.lianjia.com/ershoufang/yuhang/bp300ep370/",
        "https://hz.lianjia.com/ershoufang/yuhang/bp370ep500/",
        "https://hz.lianjia.com/ershoufang/yuhang/bp500ep100000/",

        "https://hz.lianjia.com/ershoufang/xiaoshan/ep200/",
        "https://hz.lianjia.com/ershoufang/xiaoshan/bp200ep300/",
        "https://hz.lianjia.com/ershoufang/xiaoshan/bp300ep500/",
        "https://hz.lianjia.com/ershoufang/xiaoshan/bp500ep100000/",

        "https://hz.lianjia.com/ershoufang/xiaoshan/ep200/",
        "https://hz.lianjia.com/ershoufang/xiaoshan/bp200ep300/",
        "https://hz.lianjia.com/ershoufang/xiaoshan/bp300ep500/",
        "https://hz.lianjia.com/ershoufang/xiaoshan/bp500ep100000/",

        "https://hz.lianjia.com/ershoufang/fuyang/ep200/",
        "https://hz.lianjia.com/ershoufang/fuyang/bp200ep300/",
        "https://hz.lianjia.com/ershoufang/fuyang/bp300ep500/",
        "https://hz.lianjia.com/ershoufang/fuyang/bp500ep100000/",

        "https://hz.lianjia.com/ershoufang/linan/ep200/",
        "https://hz.lianjia.com/ershoufang/linan/bp200ep300/",
        "https://hz.lianjia.com/ershoufang/linan/bp300ep500/",
        "https://hz.lianjia.com/ershoufang/linan/bp500ep100000/",

        "https://hz.lianjia.com/ershoufang/qiantangxinqu/ep200/",
        "https://hz.lianjia.com/ershoufang/qiantangxinqu/bp200ep300/",
        "https://hz.lianjia.com/ershoufang/qiantangxinqu/bp300ep500/",
        "https://hz.lianjia.com/ershoufang/qiantangxinqu/bp500ep100000/",

        "https://su.lianjia.com/ershoufang/gongyeyuan/ep200/",
        "https://su.lianjia.com/ershoufang/gongyeyuan/bp200ep300/",
        "https://su.lianjia.com/ershoufang/gongyeyuan/bp300ep500/",
        "https://su.lianjia.com/ershoufang/gongyeyuan/bp500ep100000/",

        "https://su.lianjia.com/ershoufang/wuzhong/ep200/",
        "https://su.lianjia.com/ershoufang/wuzhong/bp200ep300/",
        "https://su.lianjia.com/ershoufang/wuzhong/bp300ep500/",
        "https://su.lianjia.com/ershoufang/wuzhong/bp500ep100000/",

        "https://su.lianjia.com/ershoufang/gusu/ep200/",
        "https://su.lianjia.com/ershoufang/gusu/bp200ep300/",
        "https://su.lianjia.com/ershoufang/gusu/bp300ep500/",
        "https://su.lianjia.com/ershoufang/gusu/bp500ep100000/",

        "https://su.lianjia.com/ershoufang/gaoxin1/ep200/",
        "https://su.lianjia.com/ershoufang/gaoxin1/bp200ep300/",
        "https://su.lianjia.com/ershoufang/gaoxin1/bp300ep500/",
        "https://su.lianjia.com/ershoufang/gaoxin1/bp500ep100000/",

        "https://su.lianjia.com/ershoufang/wujiang/ep200/",
        "https://su.lianjia.com/ershoufang/wujiang/bp200ep300/",
        "https://su.lianjia.com/ershoufang/wujiang/bp300ep500/",
        "https://su.lianjia.com/ershoufang/wujiang/bp500ep100000/",

        "https://su.lianjia.com/ershoufang/xiangcheng/ep200/",
        "https://su.lianjia.com/ershoufang/xiangcheng/bp200ep300/",
        "https://su.lianjia.com/ershoufang/xiangcheng/bp300ep500/",
        "https://su.lianjia.com/ershoufang/xiangcheng/bp500ep100000/",

        "https://su.lianjia.com/ershoufang/kunshan/ep150/",
        "https://su.lianjia.com/ershoufang/kunshan/bp150ep200/",
        "https://su.lianjia.com/ershoufang/kunshan/bp200ep300/",
        "https://su.lianjia.com/ershoufang/kunshan/bp300ep100000/"

    ]

    def parse(self, response):
        self.proxy = MongoDBProxy()
        homesearch = response.xpath('//div[@class="content "]//div[@class="leftContent"]')   
        items = []
        for sel in homesearch.xpath('ul/li'):
            item = HousePriceItem()
            lianjia_id = sel.xpath('a[@class="noresultRecommend img LOGCLICKDATA"]/@data-housecode').extract_first()
            community_url = sel.xpath('div[@class="info clear"]/div[@class="address"]/div[@class="houseInfo"]/a/@href').extract_first()
            community_id = community_url.split('xiaoqu/')[1].split('/')[0]
            
            item['house_id'] = lianjia_id      
            item['capture_time'] = time.strftime("%Y%m%d%H%M%S", time.localtime())  
            item['unit_price'] = sel.xpath('div[@class="info clear"]/div[@class="priceInfo"]/div[@class="unitPrice"]/@data-price').extract_first()     
            item['total_price'] = sel.xpath('div[@class="info clear"]/div[@class="priceInfo"]/div[@class="totalPrice"]/span/text()').extract_first()   
                
            followInfo = sel.xpath('div[@class="info clear"]/div[@class="followInfo"]/text()').extract_first()
            item['follow_total'] = followInfo.split('人关注')[0]   
            item['view_total'] = '0' #暂时无法获取该数字   
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
                url = response.url.split('/ershoufang/')[0] + pageUrl.replace("{page}", str(cur_page))
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
