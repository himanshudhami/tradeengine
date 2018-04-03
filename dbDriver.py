import logging
import pymongo
import datetime
import time
import poloniex

class DbDriver:
    def __init__(self, host, db):
        self.log = logging.getLogger('DbDriver')
        self.mc = pymongo.MongoClient(host)
        self.db = self.mc[db]

    def go(self, strategy):
        dbr = self.db.ticker.find()
        i = 0
        for item in dbr:
            if i % 2 != 0:
                continue
            strategy.poll(item['value'])
            # try:
            #     strategy.poll(item['value'])
            # except Exception as e:
            #     self.log.error(e)
