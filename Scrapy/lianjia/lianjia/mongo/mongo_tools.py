from pymongo import MongoClient
import  datetime 

house_item_set = 'house_item_set'
community_item_set = 'community_item_set'
house_price_item_set = 'house_price_item_set'
transaction_item_set = 'transaction_item_set'
histroy_transaction_item_set = 'histroy_transaction_item_set'
db_name = 'house_db'

class MongoDBProxy(object):
    def __init__(self):
        self.conn = MongoClient('127.0.0.1', 27017, connect=False)
        self.db = self.conn[db_name]
        #self.db[house_item_set].ensure_index('house_id', unique=True)
        #self.db[community_item_set].ensure_index('community_id', unique=True)
        #self.db[house_price_item_set].ensure_index('house_id', unique=True)
        #self.db[house_price_item_set].ensure_index('capture_time', unique=False)
        #self.db[transaction_item_set].ensure_index('house_id', unique=True)
        #self.db[histroy_transaction_item_set].ensure_index('house_id', unique=True)

    def get_house_item(self, house_id):
        house = {"house_id" : house_id}
        item = self.db[house_item_set].find_one(house)
        return item

    def insert_house_item(self, items):
        self.db[house_item_set].insert(items)

    def get_community_item(self, community_id):
        community = {"community_id" : community_id}
        item = self.db[community_item_set].find_one(community)
        return item

    def insert_community_item(self, items):
        self.db[community_item_set].insert(items)

    def insert_house_price_item(self, items):
        self.db[house_price_item_set].insert(items)

    def is_house_transaction_item_exist(self, house_id, transaction_date):
        if house_id == "103101803404" :
            date = "2018-04-01"
        transaction = {"house_id" : house_id}
        items = self.db[transaction_item_set].find(transaction)
        for item in items:
            db_time = datetime.datetime.strptime(item["transaction_date"], "%Y-%m-%d")
            transaction_time = datetime.datetime.strptime(transaction_date, "%Y%m%d")
            minus = abs(transaction_time - db_time)
            if minus.days < 180:
                return True
        return False

    def insert_house_transaction_item(self, items):
        self.db[transaction_item_set].insert(items)
