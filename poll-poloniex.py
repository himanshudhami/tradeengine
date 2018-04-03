#!/usr/bin/env python

import pymongo
import datetime
import time
import poloniex

mc = pymongo.MongoClient('blink')
db = mc['tep-poloniex']

apiKey = ''
secret = ''
p = poloniex.poloniex(apiKey, secret)

while True:
    try:
        ticker = p.returnTicker()
        dbr = db.ticker.insert_one({ 'ts': datetime.datetime.now(), 'value': ticker })
    except Exception as e:
        print e
    finally:
        time.sleep(30)
